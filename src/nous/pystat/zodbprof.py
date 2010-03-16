#
from decorator import decorator
from nous.pystat import record_sample, reset, display


@decorator
def zodbprof(fn, *args, **kw):
    from ZODB.Connection import Connection
    old_setstate = Connection.setstate

    def monkey_setstate(self, obj):
        pickle, serial = obj._p_jar._storage.load(obj._p_oid, self._version)
        size = len(pickle)
        record_sample(**{str(type(obj)): 1,
                         'size': size})
        return old_setstate(self, obj)
    try:
        reset()
        Connection.setstate = monkey_setstate
        return fn(*args, **kw)
    finally:
        display()
        Connection.setstate = old_setstate
