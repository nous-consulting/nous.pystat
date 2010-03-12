#
from decorator import decorator

@decorator
def zodbprof(fn, *args, **kw):
    from ZODB.Connection import Connection
    old_setstate = Connection.setstate
    from collections import defaultdict
    COUNTERS = defaultdict(int)
    def monkey_setstate(self, obj):
        COUNTERS[type(obj)] += 1
        return old_setstate(self, obj)
    try:
        Connection.setstate = monkey_setstate
        return fn(*args, **kw)
    finally:
        Connection.setstate = old_setstate
        stats = sorted(COUNTERS.items(), key=lambda (k, v): v, reverse=True)
        for k, v in stats[:20]:
            print "%-10d %s" % (v, k)
