import os.path
from collections import defaultdict


###########################################################################
## Collection data structures

class ProfileState(object):
    def __init__(self, frequency=None):
        self.reset(frequency)

    def reset(self, frequency=None):
        # total so far
        self.accumulated_time = 0.0
        # start_time when timer is active
        self.last_start_time = None
        # total count of sampler calls
        self.sample_count = 0
        # a float
        if frequency:
            self.sample_interval = 1.0/frequency
        elif not hasattr(self, 'sample_interval'):
            # default to 100 Hz
            self.sample_interval = 1.0/100.0
        else:
            # leave the frequency as it was
            pass
        self.remaining_prof_time = None
        # for user start/stop nesting
        self.profile_level = 0
        # whether to catch apply-frame
        self.count_calls = False
        # gc time between start() and stop()
        self.gc_time_taken = 0

    def accumulate_time(self, stop_time):
        self.accumulated_time += stop_time - self.last_start_time

state = ProfileState()

## call_data := { code object: CallData }
call_data = {}
class CallData(object):
    def __init__(self, code):
        self.name = code.co_name
        self.filename = code.co_filename
        self.lineno = code.co_firstlineno
        self.call_count = 0
        self.cum_sample_count = 0
        self.self_sample_count = 0
        self.d_self_sample_count = defaultdict(int)
        self.d_cum_sample_count = defaultdict(int)
        call_data[code] = self

def get_call_data(code):
    return call_data.get(code, None) or CallData(code)


###########################################################################
## Reporting API

class CallStats(object):
    def __init__(self, call_data):
        self_samples = call_data.self_sample_count
        cum_samples = call_data.cum_sample_count
        nsamples = state.sample_count
        secs_per_sample = state.accumulated_time / nsamples
        basename = os.path.basename(call_data.filename)

        self.name = '%s:%d:%s' % (basename, call_data.lineno, call_data.name)
        self.pcnt_time_in_proc = self_samples / nsamples * 100
        self.cum_secs_in_proc = cum_samples * secs_per_sample
        self.self_secs_in_proc = self_samples * secs_per_sample
        self.num_calls = None
        self.self_secs_per_call = None
        self.cum_secs_per_call = None

    def display(self):
        print '%6.2f %9.2f %9.2f  %s' % (self.pcnt_time_in_proc,
                                         self.cum_secs_in_proc,
                                         self.self_secs_in_proc,
                                         self.name)

class CallStats(object):
    def __init__(self, call_data):
        self_samples = call_data.self_sample_count
        cum_samples = call_data.cum_sample_count
        nsamples = state.sample_count
        secs_per_sample = state.accumulated_time / nsamples
        basename = os.path.basename(call_data.filename)

        self.name = '%s:%d:%s' % (basename, call_data.lineno, call_data.name)
        self.pcnt_time_in_proc = self_samples / nsamples * 100
        self.cum_secs_in_proc = cum_samples * secs_per_sample
        self.self_secs_in_proc = self_samples * secs_per_sample
        self.num_calls = None
        self.self_secs_per_call = None
        self.cum_secs_per_call = None
        self.d_self_sample_count = call_data.d_self_sample_count

    def display(self):
        multi_counter_data = ""
        if self.d_self_sample_count:
            multi_counter_data = ", ".join([str(item)
                                            for item in self.d_self_sample_count.items()])

        print '%6.2f %9.2f %9.2f  %s%s' % (self.pcnt_time_in_proc,
                                           self.cum_secs_in_proc,
                                           self.self_secs_in_proc,
                                           self.name,
                                           multi_counter_data)

# Common stat api functions
def reset(frequency=None):
    call_data.clear()
    state.reset(frequency)


# XXX rewrite it so it would be generic
def display():
    if state.sample_count == 0:
        print 'No samples recorded.'
        return

    l = [CallStats(x) for x in call_data.itervalues()]
    l = [(x.self_secs_in_proc, x.cum_secs_in_proc, x) for x in l]
    l.sort(reverse=True)
    l = [x[2] for x in l]

    print '%5.5s %10.10s   %7.7s  %-8.8s' % ('%  ', 'cumulative', 'self', '')
    print '%5.5s  %9.9s  %8.8s  %-8.8s' % ("time", "seconds", "seconds", "name")

    for x in l:
        x.display()

    print '---'
    print 'Sample count: %d' % state.sample_count
    print 'Total time: %f seconds' % state.accumulated_time
