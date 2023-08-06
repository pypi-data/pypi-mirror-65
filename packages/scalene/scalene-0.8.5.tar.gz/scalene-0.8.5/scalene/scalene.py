"""Scalene: a high-performance, high-precision CPU *and* memory profiler for Python.

    Scalene uses interrupt-driven sampling for CPU profiling. For memory
    profiling, it uses a similar mechanism but with interrupts generated
    by a "sampling memory allocator" that produces signals everytime the
    heap grows or shrinks by a certain amount. See libscalene.cpp for
    details (sampling logic is in include/sampleheap.hpp).

    by Emery Berger
    https://emeryberger.com

    usage: # for CPU profiling only
            python -m Scalene test/testme.py
            # for CPU and memory profiling (Mac OS X)
            DYLD_INSERT_LIBRARIES=$PWD/libscalene.dylib PYTHONMALLOC=malloc python -m scalene test/testme.py
            # for CPU and memory profiling (Linux)
            LD_PRELOAD=$PWD/libscalene.so PYTHONMALLOC=malloc python -m scalene test/testme.py

"""

import contextlib
import dis
import traceback
import sys
import atexit
import signal
import math
import random
import threading
from collections import defaultdict
import time
from pathlib import Path
import os
import argparse
from contextlib import contextmanager
from functools import lru_cache
from textwrap import dedent

from . import adaptive # reservoir
from . import sparkline

# Logic to ignore @profile decorators.
import builtins
try:
    builtins.profile
except AttributeError:
    # No line profiler, provide a pass-through version
    def profile(func): return func
    builtins.profile = profile


the_globals = {
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': globals()['__loader__'],
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': globals()['__builtins__'],
    '__file__': None,
    '__cached__': None,
}

assert sys.version_info[0] == 3 and sys.version_info[1] >= 5, "Scalene requires Python version 3.5 or above."

# Scalene currently only supports Unix-like operating systems; in particular, Linux and Mac OS X.
if sys.platform == 'win32':
    print("Scalene currently does not support Windows, but works on Linux and Mac OS X.")
    sys.exit(-1)

    
class Scalene():
    """The Scalene profiler itself."""

    # We use these in is_call_function to determine whether a particular bytecode is a function call.
    # We use this to distinguish between Python and native code execution when running in threads.
    call_opcodes                  = { dis.opmap[op_name] for op_name in dis.opmap if op_name.startswith("CALL_FUNCTION") }

    # Cache the original thread join function, which we replace with our own version.
    original_thread_join          = threading.Thread.join
    
    # Statistics counters.
    cpu_samples_python            = defaultdict(lambda: defaultdict(float))  # CPU    samples for each location in the program
                                                                             #        spent in the interpreter
    cpu_samples_c                 = defaultdict(lambda: defaultdict(float))  # CPU    samples for each location in the program
                                                                             #        spent in C / libraries / system calls

    # Below are indexed by [filename][line_no][bytecode_index].
    # malloc samples for each location in the program
    memory_malloc_samples         = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    # number of times samples were added for the above
    memory_malloc_count           = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # free samples for each location in the program
    memory_free_samples           = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    # number of times samples were added for the above
    memory_free_count             = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # memcpy samples for each location in the program
    memcpy_samples                = defaultdict(lambda: defaultdict(int))
    # max malloc samples for each location in the program
    memory_max_samples            = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    total_max_samples             = 0
    total_cpu_samples             = 0.0            # how many CPU    samples have been collected.
    total_memory_malloc_samples   = 0              # "   "    malloc "       "    "    "
    total_memory_free_samples     = 0              # "   "    free   "       "    "    "
    current_footprint             = 0              # the current memory footprint.
    max_footprint                 = 0              # the peak memory footprint.
    
    mean_signal_interval          = 0.01 # sys.getswitchinterval() # 0.01           # mean seconds between interrupts for CPU sampling.
    last_signal_interval          = mean_signal_interval    # last num seconds between interrupts for CPU sampling.

    memory_footprint_samples      = adaptive.adaptive(27) # reservoir.reservoir(47)  # memory footprint samples (time, footprint), using reservoir sampling.
    # per_line_footprint_samples    = defaultdict(lambda: defaultdict(lambda: reservoir.reservoir(10)))
    per_line_footprint_samples    = defaultdict(lambda: defaultdict(lambda: adaptive.adaptive(9)))
    
    # total_memory_samples          = 0              # total memory samples so far.

    original_path                 = ""             # original working directory.
    program_path                  = ""             # path for the program being profiled.
    output_file                   = ""             # where we write profile info.
    output_profile_interval       = float("inf")   # how long between outputting stats during execution.
    next_output_time              = float("inf")   # when do we output the next profile.
    elapsed_time                  = 0              # total time spent in program being profiled.
    bytei_map                     = defaultdict(lambda: defaultdict(lambda: set())) # [filename][lineno] -> set(byteindex)
    
    # Things that need to be in sync with include/sampleheap.hpp:

    malloc_signal_filename        = "/tmp/scalene-malloc-signal"             # file to communicate the number of malloc/free samples (+ PID)
    memcpy_signal_filename        = "/tmp/scalene-memcpy-signal"             # file to communicate the number of memcpy samples (+ PID)
    
    # The specific signals we use. Malloc and free signals are generated by include/sampleheap.hpp.

    cpu_signal    = signal.SIGVTALRM
    malloc_signal = signal.SIGXCPU
    free_signal   = signal.SIGXFSZ
    memcpy_signal = signal.SIGPROF

    # Program-specific information.
    program_being_profiled = ""          # the name of the program being profiled.
    program_path           = ""          # the path "  "   "       "     "



    @staticmethod
    @lru_cache(1024)
    def is_call_function(code, bytei):
        """Returns true iff the bytecode at the given index is a function call."""
        for ins in dis.get_instructions(code):
            if ins.offset == bytei:
                if ins.opcode in Scalene.call_opcodes:
                    return True
        return False

        
    @staticmethod
    def thread_join_replacement(self, timeout=None):
        """We replace threading.Thread.join with this method which always periodically yields."""
        start_time = Scalene.gettime()
        interval   = sys.getswitchinterval()
        while self.is_alive():
            Scalene.original_thread_join(self, interval)
            # If a timeout was specified, check to see if it's expired.
            if timeout:
                end_time = Scalene.gettime()
                if end_time - start_time >= timeout:
                    return None
        return None
    
    @staticmethod
    def set_timer_signal(use_wallclock_time = False):
        """Set up timer signals for CPU profiling."""
        if use_wallclock_time:
            Scalene.cpu_timer_signal = signal.ITIMER_REAL
        else:
            Scalene.cpu_timer_signal = signal.ITIMER_VIRTUAL
            
        # Now set the appropriate timer signal.
        if Scalene.cpu_timer_signal == signal.ITIMER_REAL:
            Scalene.cpu_signal  = signal.SIGALRM
        elif Scalene.cpu_timer_signal == signal.ITIMER_VIRTUAL:
            Scalene.cpu_signal = signal.SIGVTALRM
        elif Scalene.cpu_timer_signal == signal.ITIMER_PROF:
            # NOT SUPPORTED
            assert False, "ITIMER_PROF is not currently supported."

    @staticmethod
    def enable_signals():
        """Set up the signal handlers to handle interrupts for profiling and start the timer interrupts."""
        # CPU
        signal.signal(Scalene.cpu_signal, Scalene.cpu_signal_handler)
        # malloc/free interrupts (for memory allocations).
        signal.signal(Scalene.malloc_signal, Scalene.malloc_event_signal_handler)
        signal.signal(Scalene.free_signal, Scalene.free_event_signal_handler)
        signal.signal(Scalene.memcpy_signal, Scalene.memcpy_event_signal_handler)
        # Turn on the CPU profiling timer to run every signal_interval seconds.
        signal.setitimer(Scalene.cpu_timer_signal, Scalene.mean_signal_interval, Scalene.mean_signal_interval)
        Scalene.last_signal_time = Scalene.gettime()
        
    
    @staticmethod
    def gettime():
        """High-precision timer of time spent running in or on behalf of this process."""
        return time.process_time()

    def __init__(self, program_being_profiled=None):
        # Hijack join.
        threading.Thread.join = Scalene.thread_join_replacement
        # Build up signal filenames (adding PID to each).
        Scalene.malloc_signal_filename += str(os.getpid());
        Scalene.memcpy_signal_filename += str(os.getpid());
        # Register the exit handler to run when the program terminates or we quit.
        atexit.register(Scalene.exit_handler)
        # Store relevant names (program, path).
        if program_being_profiled:
            Scalene.program_being_profiled = os.path.abspath(program_being_profiled)
            Scalene.program_path = os.path.dirname(Scalene.program_being_profiled)

    @staticmethod
    def cpu_signal_handler(_, this_frame):
        """Handle interrupts for CPU profiling."""
        # Record how long it has been since we received a timer
        # before.  See the logic below.
        now = Scalene.gettime()
        # If it's time to print some profiling info, do so.
        if now >= Scalene.next_output_time:
            # Print out the profile.
            # Set the next output time, stop signals, print the profile, and then start signals again.
            Scalene.next_output_time += Scalene.output_profile_interval
            Scalene.stop()
            Scalene.output_profiles()
            Scalene.start()
        # Here we take advantage of an ostensible limitation of Python:
        # it only delivers signals after the interpreter has given up
        # control. This seems to mean that sampling is limited to code
        # running purely in the interpreter, and in fact, that was a limitation
        # of the first version of Scalene, meaning that native code was entirely ignored.
        #
        # (cf. https://docs.python.org/3.9/library/signal.html#execution-of-python-signal-handlers)
        #
        # However: lemons -> lemonade: this "problem" is in fact
        # an effective way to separate out time spent in
        # Python vs. time spent in native code "for free"!  If we get
        # the signal immediately, we must be running in the
        # interpreter. On the other hand, if it was delayed, that means
        # we are running code OUTSIDE the interpreter, e.g.,
        # native code (be it inside of Python or in a library). We
        # account for this time by tracking the elapsed (process) time
        # and compare it to the interval, and add any computed delay
        # (as if it were sampled) to the C counter.
        elapsed      = now - Scalene.last_signal_time
        python_time  = Scalene.last_signal_interval
        c_time       = elapsed - python_time
        #print(f"elapsed: {elapsed} + python: {python_time} + c_time: {c_time}")
        if c_time < 0:
            c_time = 0
        # Update counters for every running thread.

    
        frames = [this_frame]

        frames = [sys._current_frames().get(t.ident, None) for t in threading.enumerate()]
        frames.append(this_frame)

        # Process all the frames to remove ones we aren't going to track.
        new_frames = []
        for frame in frames:
            if frame is None:
                continue
            fname = frame.f_code.co_filename
            # Record samples only for files we care about.
            if (len(fname)) == 0:
                # 'eval/compile' gives no f_code.co_filename.
                # We have to look back into the outer frame in order to check the co_filename.
                fname = frame.f_back.f_code.co_filename
            if not Scalene.should_trace(fname):
                continue
            new_frames.append(frame)
            
        del frames
    
        # Now update counters (weighted) for every frame we are tracking.
        total_time = python_time + c_time
        
        for frame in new_frames:
            fname = frame.f_code.co_filename
            if frame == this_frame:
                # Main thread.
                Scalene.cpu_samples_python[fname][frame.f_lineno] += python_time / len(new_frames)
                Scalene.cpu_samples_c[fname][frame.f_lineno]      += c_time / len(new_frames)
            else:
                # We can't play the same game here of attributing
                # time, because we are in a thread, and threads don't
                # get signals in Python. Instead, we check if the
                # bytecode instruction being executed is a function
                # call.  If so, we attribute all the time to native.
                if Scalene.is_call_function(frame.f_code, frame.f_lasti):
                    # Attribute time to native.
                    Scalene.cpu_samples_c[fname][frame.f_lineno] += total_time / len(new_frames)
                else:
                    # Not in a call function so we attribute the time to Python.
                    Scalene.cpu_samples_python[fname][frame.f_lineno] += total_time / len(new_frames)
            # Roll memory usage info into the per-line footprint samples (for later printing as sparklines).
            #growth = 0
            #for index in Scalene.bytei_map[fname][frame.f_lineno]:
            #    memory_delta = Scalene.memory_malloc_samples[fname][frame.f_lineno][index] - Scalene.memory_free_samples[fname][frame.f_lineno][index]
            #    growth += memory_delta

        del new_frames
        
        Scalene.total_cpu_samples += total_time

        # total_samples_to_record = int(round(elapsed / Scalene.last_signal_interval, 0))
        
        # Reservoir sampling to get an even distribution of footprints over time.
        #for i in range(0, total_samples_to_record):
        #    Scalene.memory_footprint_samples.add([now, Scalene.current_footprint])
        
        # disabled randomness for now
        # Scalene.last_signal_interval = random.uniform(Scalene.mean_signal_interval / 2, Scalene.mean_signal_interval * 3 / 2)
        # signal.setitimer(Scalene.cpu_timer_signal, Scalene.last_signal_interval, Scalene.last_signal_interval)
        Scalene.last_signal_time = Scalene.gettime()
        return

    @staticmethod
    def compute_frames_to_record(this_frame):
        frames = [this_frame]
        frames += [sys._current_frames().get(t.ident, None) for t in threading.enumerate()]
        # Process all the frames to remove ones we aren't going to track.
        new_frames = []
        for frame in frames:
            if frame is None:
                continue
            fname = frame.f_code.co_filename
            # Record samples only for files we care about.
            if (len(fname)) == 0:
                # 'eval/compile' gives no f_code.co_filename.
                # We have to look back into the outer frame in order to check the co_filename.
                fname = frame.f_back.f_code.co_filename
            if not Scalene.should_trace(fname):
                continue
            new_frames.append(frame)
        return new_frames
        

    @staticmethod
    def allocation_handler(this_frame):
        """Handle interrupts for memory profiling (mallocs and frees)."""
        new_frames = Scalene.compute_frames_to_record(this_frame)

        if len(new_frames) == 0:
            return

        # Process the input array.
        arr = []
        try:
            with open(Scalene.malloc_signal_filename, "r") as f:
                for l, count_str in enumerate(f, 1):
                    count_str = count_str.rstrip()
                    (action, alloc_time, count) = count_str.split(',')
                    arr.append([int(alloc_time), action, float(count)])
        except FileNotFoundError:
            pass
        try:
            os.remove(Scalene.malloc_signal_filename)
        except FileNotFoundError:
            pass
        arr.sort()

        # Iterate through the array to compute the new current footprint.
        # and update the global memory_footprint_samples.
        before = Scalene.current_footprint
        for item in arr:
            alloc_time, action, count = item
            # print(fname,line_no,action, alloc_time, count)
            count /= (1024 * 1024)
            is_malloc = action == "M"
            if is_malloc:
                Scalene.current_footprint += count
                if Scalene.current_footprint > Scalene.max_footprint:
                    Scalene.max_footprint = Scalene.current_footprint
            else:
                Scalene.current_footprint -= count
            Scalene.memory_footprint_samples.add(Scalene.current_footprint)
        after = Scalene.current_footprint

        # Now update the memory footprint for every running frame.
        # This is a pain, since we don't know to whom to attribute memory,
        # so we may overcount.
        num_threads = len(new_frames)
        
        for frame in new_frames:
            fname  = frame.f_code.co_filename
            line_no = frame.f_lineno
            bytei = frame.f_lasti
            # Add the byte index to the set for this line.
            if bytei not in Scalene.bytei_map[fname][line_no]:
                Scalene.bytei_map[fname][line_no].add(bytei)
            curr = before
            # Go through the array again and add each updated current footprint.
            for item in arr:
                alloc_time, action, count = item
                count /= (1024 * 1024)
                is_malloc = action == "M"
                if is_malloc:
                    curr += count
                else:
                    curr -= count
                Scalene.per_line_footprint_samples[fname][line_no].add(curr)
            assert curr == after
            # If there was a net increase in memory, treat it as if it was a malloc; otherwise, treat it as if it was a free.
            # This is for later reporting of net memory gain / loss per line of code.
            #print(fname + ":" + str(line_no) + " = " + str(after - before))
            if after > before:
                Scalene.memory_malloc_samples[fname][line_no][bytei] += (after - before)# / num_threads
                Scalene.memory_malloc_count[fname][line_no][bytei] += 1 #/ num_threads
                Scalene.total_memory_malloc_samples += (after - before)# / num_threads
            else:
                Scalene.memory_free_samples[fname][line_no][bytei] += (before - after)# / num_threads
                Scalene.memory_free_count[fname][line_no][bytei] += 1 #/ num_threads
                Scalene.total_memory_free_samples += (before - after) #/ num_threads
    

    @staticmethod
    def malloc_event_signal_handler(_, frame):
        Scalene.allocation_handler(frame)


    @staticmethod
    def free_event_signal_handler(_, frame):
        Scalene.allocation_handler(frame)
        
    @staticmethod
    def memcpy_event_signal_handler(_, frame):
        new_frames = Scalene.compute_frames_to_record(frame)
        if len(new_frames) == 0:
            return

        # Process the input array.
        arr = []
        try:
            with open(Scalene.memcpy_signal_filename, "r") as f:
                for l, count_str in enumerate(f, 1):
                    count_str = count_str.rstrip()
                    (memcpy_time, count) = count_str.split(',')
                    arr.append([int(memcpy_time), int(count)])
        except FileNotFoundError:
            pass
        try:
            os.remove(Scalene.memcpy_signal_filename)
        except FileNotFoundError:
            pass
        arr.sort()
            
        num_threads = len(new_frames)

        for item in arr:
            memcpy_time, count = item
            for frame in new_frames:
                fname  = frame.f_code.co_filename
                line_no = frame.f_lineno
                bytei = frame.f_lasti
                # Add the byte index to the set for this line.
                if bytei not in Scalene.bytei_map[fname][line_no]:
                    Scalene.bytei_map[fname][line_no].add(bytei)
                Scalene.memcpy_samples[fname][line_no] += count
        # Scalene.allocation_handler(frame)
        

    @staticmethod
    @lru_cache(128)
    def should_trace(filename):
        """Return true if the filename is one we should trace."""
        # Profile anything in the program's directory or a child directory,
        # but nothing else.
        if filename[0] == '<' or 'site-packages' in filename or '/usr/lib/python' in filename:
            # Don't profile Python internals.
            return False
        if 'scalene.py' in filename or 'adaptive.py' in filename:
            # Don't profile the profiler.
            return False
        filename = os.path.abspath(filename)
        return Scalene.program_path in filename

    @staticmethod
    def start():
        """Initiate profiling."""
        os.chdir(Scalene.program_path)
        Scalene.enable_signals()
        Scalene.elapsed_time = Scalene.gettime()

    @staticmethod
    def stop():
        """Complete profiling."""
        Scalene.disable_signals()
        Scalene.elapsed_time = Scalene.gettime() - Scalene.elapsed_time
        os.chdir(Scalene.original_path) 

    @staticmethod
    @contextmanager
    def file_or_stdout(file_name):
        """Returns a file handle for writing; if no argument is passed, returns stdout."""
        # from https://stackoverflow.com/questions/9836370/fallback-to-stdout-if-no-file-name-provided
        if file_name is None:
            yield sys.stdout
        else:
            with open(file_name, 'w') as out_file:
                yield out_file

    @staticmethod
    def generate_sparkline(arr, minimum=-1, maximum=-1):
        iterations = len(arr)
        # Sort samples by time.
        # arr.sort()
        # Prevent negative memory output due to sampling error.
        # samples = [i if i > 0 else 0 for [t, i] in arr]
        all_zeros = all([i == 0 for i in arr])
        if all_zeros:
            return 0, 0, ""
        samples = [i if i > 0 else 0 for i in arr]
        # Force the y-axis to start at 0.
        # samples = [0, 0] + samples
        mn, mx, sp = sparkline.sparkline(samples[0:iterations], minimum, maximum)
        return mn, mx, sp
        
    @staticmethod
    def output_profiles():
        """Write the profile out (currently to stdout)."""
        current_max = Scalene.max_footprint
        # print(current_max)
        # If we've collected any samples, dump them.
        if Scalene.total_cpu_samples == 0 and Scalene.total_memory_malloc_samples == 0 and Scalene.total_memory_free_samples == 0:
            # Nothing to output.
            return False
        # If I have at least one memory sample, then we are profiling memory.
        did_sample_memory = (Scalene.total_memory_free_samples + Scalene.total_memory_malloc_samples) > 0
        # Collect all instrumented filenames.
        all_instrumented_files = list(set(list(Scalene.cpu_samples_python.keys()) + list(Scalene.cpu_samples_c.keys()) + list(Scalene.memory_free_samples.keys()) + list(Scalene.memory_malloc_samples.keys())))
        with Scalene.file_or_stdout(Scalene.output_file) as out:
            if did_sample_memory:
                if len(Scalene.memory_footprint_samples.get()) > 0:
                    # Output a sparkline as a summary of memory usage over time.
                    mn, mx, sp = Scalene.generate_sparkline(Scalene.memory_footprint_samples.get()[0:Scalene.memory_footprint_samples.len()], 0, current_max)
                    print("Memory usage: " + sp + " (max: %6.2fMB)" % current_max, file=out)
                    # print("min: %6.2fMB, max: %6.2fMB" % (mn, mx), file=out)
                    
            for fname in sorted(all_instrumented_files):

                this_cpu_samples = sum(Scalene.cpu_samples_c[fname].values()) + sum(Scalene.cpu_samples_python[fname].values())

                try:
                    percent_cpu_time = 100 * this_cpu_samples / Scalene.total_cpu_samples
                except ZeroDivisionError:
                    percent_cpu_time = 0

                # Print header.
                # percent_cpu_time = 100 * this_cpu_samples * Scalene.mean_signal_interval / Scalene.elapsed_time
                print("%s: %% of CPU time = %6.2f%% out of %6.2fs." % (fname, percent_cpu_time, Scalene.elapsed_time), file=out)

                print("       |%9s |%9s | %s %s %s" % ('CPU %', 'CPU %', ' Net  |' if did_sample_memory else '', 'Memory usage   |' if did_sample_memory else '', 'Copy  |' if did_sample_memory else ''), file=out)
                print("  Line |%9s |%9s | %s %s %s [%s]" % ('(Python)', '(native)', ' (MB) |' if did_sample_memory else '', 'over time /  % |' if did_sample_memory else '', '(MB/s)|' if did_sample_memory else '', fname), file=out)
                print("-" * 80, file=out)

                with open(fname, 'r') as source_file:
                    for line_no, line in enumerate(source_file, 1):
                        line = line.rstrip() # Strip newline
                        # Prepare output values.
                        n_cpu_samples_c = Scalene.cpu_samples_c[fname][line_no]
                        # Correct for negative CPU sample counts.
                        # This can happen because of floating point inaccuracies, since we perform subtraction to compute it.
                        if n_cpu_samples_c < 0:
                            n_cpu_samples_c = 0
                        n_cpu_samples_python = Scalene.cpu_samples_python[fname][line_no]
                        
                        # Compute percentages of CPU time.
                        if Scalene.total_cpu_samples != 0:
                            n_cpu_percent_c = n_cpu_samples_c * 100 / Scalene.total_cpu_samples
                            n_cpu_percent_python = n_cpu_samples_python * 100 / Scalene.total_cpu_samples
                        else:
                            n_cpu_percent_c = 0
                            n_cpu_percent_python = 0
                            
                        # Now, memory stats.
                        # Accumulate each one from every byte index.
                        n_malloc_mb = 0
                        n_free_mb = 0
                        n_avg_malloc_mb = 0
                        n_avg_free_mb = 0
                        n_malloc_count = 0
                        n_free_count = 0
                        for index in Scalene.bytei_map[fname][line_no]:
                            # print(fname,line_no,index)
                            mallocs         = Scalene.memory_malloc_samples[fname][line_no][index]
                            n_malloc_mb     += mallocs
                            n_malloc_count  += Scalene.memory_malloc_count[fname][line_no][index]
                            frees           = Scalene.memory_free_samples[fname][line_no][index]
                            n_free_mb       += frees
                            n_free_count    += Scalene.memory_free_count[fname][line_no][index]

                            if n_malloc_count > 0:
                                n_avg_malloc_mb += mallocs / n_malloc_count
                            if n_free_count > 0:
                                n_avg_free_mb   += frees / n_free_count
                            
                        #n_growth_mb = n_malloc_mb - n_free_mb
                        #print("mallocs " + str(n_malloc_mb))
                        #print("frees " + str(n_free_mb))
                        n_growth_mb = n_malloc_mb - n_free_mb
                        if (n_growth_mb < 0) and (n_growth_mb > -1):
                            # Don't print out "-0".
                            n_growth_mb = 0
                        # n_usage_fraction = 0 if Scalene.total_memory_malloc_samples == 0 else n_avg_free_mb
                        #n_usage_fraction = 0 if Scalene.total_memory_malloc_samples == 0 else (n_avg_malloc_mb) / (Scalene.total_memory_malloc_samples)
                        n_usage_fraction = 0 if Scalene.total_memory_malloc_samples == 0 else n_malloc_mb / Scalene.total_memory_malloc_samples
                        # Finally, print results.
                        n_cpu_percent_c_str = "" if n_cpu_percent_c == 0 else '%6.2f%%' % n_cpu_percent_c
                        n_cpu_percent_python_str = "" if n_cpu_percent_python == 0 else '%6.2f%%' % n_cpu_percent_python
                        n_avg_malloc_mb_str = "" if (n_avg_malloc_mb == 0 and n_usage_fraction == 0) else '%5.0f' % n_avg_malloc_mb
                        n_growth_mb_str  = "" if (n_growth_mb == 0 and n_usage_fraction == 0) else '%5.0f' % n_growth_mb
                        # n_usage_fraction_str  = "" if n_usage_fraction == 0 else '%11.0f' % n_usage_fraction
                        n_usage_fraction_str  = "" if n_usage_fraction == 0 else '%3.0f%%' % (100 * n_usage_fraction)
                        # n_usage_fraction_str  = n_avg_free_mb_str # "" if n_usage_fraction == 0 else '%9.2f%%' % (100 * n_usage_fraction)
                        n_copy_b = Scalene.memcpy_samples[fname][line_no]
                        n_copy_mb_s = n_copy_b / (1024 * 1024 * Scalene.elapsed_time)
                        n_copy_mb_s_str = "" if n_copy_mb_s < 1 else '%6.0f' % n_copy_mb_s
                        
                        if did_sample_memory:
                            # print("%6d\t | %9s | %9s | %11s | %11s | %s" %
                            spark_string = ""
                            # Scale the sparkline by the usage fraction.
                            samples = Scalene.per_line_footprint_samples[fname][line_no]
                            for i in range(0, len(samples.get())):
                                samples.get()[i] *= n_usage_fraction
                            if len(Scalene.per_line_footprint_samples[fname][line_no].get()) > 0:
                                mn, mx, spark_string = Scalene.generate_sparkline(Scalene.per_line_footprint_samples[fname][line_no].get()[0:Scalene.per_line_footprint_samples[fname][line_no].len()], 0, current_max)
                                # print(Scalene.per_line_footprint_samples[fname][line_no].get()[0:Scalene.per_line_footprint_samples[fname][line_no].len()])
                            print("%6d |%9s |%9s | %5s | %-9s %-4s |%-6s | %s" %
                                  (line_no, n_cpu_percent_python_str, n_cpu_percent_c_str, n_growth_mb_str, spark_string, n_usage_fraction_str, n_copy_mb_s_str, line), file=out)
                        else:
                            print("%6d |%9s |%9s | %s" %
                                  (line_no, n_cpu_percent_python_str, n_cpu_percent_c_str, line), file=out)
                    print("", file=out)
        return True

        
    @staticmethod
    def disable_signals():
        """Turn off the profiling signals."""
        signal.setitimer(Scalene.cpu_timer_signal, 0)
        signal.signal(Scalene.malloc_signal, signal.SIG_IGN)
        signal.signal(Scalene.free_signal, signal.SIG_IGN)
        signal.signal(Scalene.memcpy_signal, signal.SIG_IGN)

    @staticmethod
    def exit_handler():
        """When we exit, disable all signals."""
        Scalene.disable_signals()

    @contextlib.contextmanager
    def scalene_profiler(): # TODO add memory stuff
        profiler = Scalene("")
        profiler.start()
        yield
        profiler.stop()
        profiler.output_profiles() # though this needs to be constrained

    @staticmethod
    def main():
        """Invokes the profiler from the command-line."""
        usage = dedent("""Scalene: a high-precision CPU and memory profiler.
            https://github.com/emeryberger/Scalene

                for CPU profiling only:
            % python -m scalene yourprogram.py
                for CPU and memory profiling (Mac OS X):
            % DYLD_INSERT_LIBRARIES=$PWD/libscalene.dylib PYTHONMALLOC=malloc python -m scalene yourprogram.py
                for CPU and memory profiling (Linux):
            % LD_PRELOAD=$PWD/libscalene.so PYTHONMALLOC=malloc python -m scalene yourprogram.py
            """)
        parser = argparse.ArgumentParser(prog='scalene', description=usage, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('prog', type=str, help='program to be profiled')
        parser.add_argument('-o', '--outfile', type=str, default=None, help='file to hold profiler output (default: stdout)')
        parser.add_argument('--profile-interval', type=float, default=float("inf"), help='output profiles every so many seconds.')
        parser.add_argument('--wallclock', dest='wallclock', action='store_const', const=True, default=False, help='use wall clock time (default: virtual time)')
        # Parse out all Scalene arguments and jam the remaining ones into argv.
        # See https://stackoverflow.com/questions/35733262/is-there-any-way-to-instruct-argparse-python-2-7-to-remove-found-arguments-fro
        args, left = parser.parse_known_args()
        sys.argv = sys.argv[:1]+left
        Scalene.set_timer_signal(args.wallclock)
        Scalene.output_profile_interval = args.profile_interval
        Scalene.next_output_time = Scalene.gettime() + Scalene.output_profile_interval
        try:
            with open(args.prog, 'rb') as prog_being_profiled:
                Scalene.original_path = os.getcwd()
                # Read in the code and compile it.
                code = compile(prog_being_profiled.read(), args.prog, "exec")
                # Push the program's path.
                program_path = os.path.dirname(os.path.abspath(args.prog))
                sys.path.insert(0, program_path)
                Scalene.program_path = program_path
                os.chdir(program_path) # FIXME?
                # Grab local and global variables.
                import __main__
                the_locals = __main__.__dict__
                the_globals = __main__.__dict__
                # Splice in the name of the file being executed instead of the profiler.
                the_globals['__file__'] = args.prog
                # Start the profiler.
                Scalene.output_file = args.outfile
                fullname = os.path.join(program_path, os.path.basename(args.prog))
                profiler = Scalene(fullname)
                try:
                    profiler.start()
                    # Run the code being profiled.
                    try:
                        exec(code, the_globals, the_locals)
                    except BaseException as be:
                        # Intercept sys.exit.
                        #print("base exception = " + str(be)) # FIXME
                        #print(traceback.format_exc())
                        pass
                    profiler.stop()
                    # Go back home.
                    # os.chdir(Scalene.original_path)
                    # If we've collected any samples, dump them.
                    if profiler.output_profiles():
                        pass
                    else:
                        print("Scalene: Program did not run for long enough to profile.")
                except Exception as ex:
                    template = "Scalene: An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
                    print(traceback.format_exc())
        except (FileNotFoundError, IOError):
            print("Scalene: could not find input file.")


if __name__ == "__main__":
    Scalene.main()
