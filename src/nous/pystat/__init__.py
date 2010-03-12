#
import sys
from nous.pystat.stats import (reset as reset_orig,
                               display as display_orig,
                               state, get_call_data)


from collections import defaultdict


def get_frame():
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        return sys.exc_info()[2].tb_frame.f_back


def reset():
    reset_orig()
    state.last_start_time = 0
    state.accumulated_time = 0
    state.d_accumulated_time = defaultdict(int)
    state.d_last_start_time = defaultdict(int)


def display():
    display_orig()

    # display totals for all the counters
    stats = sorted(state.d_accumulated_time.items(), key=lambda (k, v): v, reverse=True)
    for k, v in stats[:20]:
        print "%-10d %s" % (v, k)


def sample_stack_procs(frame, up=1, **counters):
    state.sample_count += 1

    # skip the setstate frame
    for i in range(up):
        frame = frame.f_back
    get_call_data(frame.f_code).self_sample_count += 1
    for name, value in counters.items():
        get_call_data(frame.f_code).d_self_sample_count[name] += value
    code_seen = {}
    while frame:
        code_seen[frame.f_code] = True
        frame = frame.f_back
    for code in code_seen.iterkeys():
        get_call_data(code).cum_sample_count += 1

    for code in code_seen.iterkeys():
        for name, value in counters.items():
            get_call_data(code).d_cum_sample_count[name] += value


def record_sample(up=1, **counters):
    frame = get_frame()
    for name, value in counters.items():
        state.d_last_start_time[name] += value
        state.d_accumulated_time[name] += value
    state.last_start_time += 1
    state.accumulate_time(state.last_start_time + 1)
    sample_stack_procs(frame, up=up+1, **counters)
