nous.pystat
===========

An extensible profiler for Python based on Andy Wingo's statprof
from http://wingolog.org/archives/2005/10/28/profiling


Installing
----------

You need Python 2.5 or newer (but Python 3.x is not supported).  Do the usual
setuptools/distutils thing, e.g. ::

    git clone git://github.com/Ignas/nous.pystat.git
    easy_install nous.pystat
    easy_install py-itimer


Profiling Python code
---------------------

This is a statistical profiler, so it should have less overhead than, say,
cProfile.  It is also not as accurate.  Most importantly, it's unsuitable
for profiling I/O-bound *or* multithreaded applications.

Usage:

    >>> from nous.pystat.statprof import start, stop, display, reset
    >>> reset() # optional
    >>> start()
    >>> ... do your computation ...
    >>> stop()
    >>> display()

This use case is unchanged from Andy Wingo's statprof, and more documentation
can be found with

    >>> help('nous.pystat.statprof')

There is one new convenience function:

    >>> from nous.pystat.statprof import run
    >>> run(function_performing_some_computation, *args, **kw).


Profiling ZODB object loads
---------------------------

This is a neat hack that monkey-patches ZODBs object load method and collects
accurate data on the number of persistent objects loaded during runtime.
Usage::

    from nous.pystat.zodbprof import zodbprof

    @zodbprof
    def my_function(...):
        ...

Every time that function is executed you'll see a summary output on stdout.
