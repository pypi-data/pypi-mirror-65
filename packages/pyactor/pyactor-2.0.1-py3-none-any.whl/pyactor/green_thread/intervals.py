from gevent.event import Event
from gevent import spawn
from gevent import sleep as gsleep


def sleep(seconds):
    """
    Facade for the sleep function. Do not use time.sleep if you are
    running green threads.

    :param  int time: time to sleep, in seconds. (Float for second
        divisions)
    """
    gsleep(seconds)


def later(timeout, f, *args, **kwargs):
    """
    Sets a timer that will call the *f* function past *timeout* seconds.

    See example in :ref:`sample_inter`

    :return: :class:`Greenlet` new 'thread' which will perform the call
        when specified.
    """
    def wrap(*args, **kwargs):
        sleep(timeout)
        return f(*args, **kwargs)

    return spawn(wrap, *args, **kwargs)


def interval_host(host, time, f, *args, **kwargs):
    """
    Creates an Event attached to the *host* that will execute the *f*
    function every *time* seconds.

    See example in :ref:`sample_inter`

    :param Proxy host: host proxy. Can be obtained from inside a
        class with ``self.host``.
    :param int time: seconds for the intervals.
    :param func f: function to be called every *time* seconds.
    :param list args: arguments for *f*.
    :return: :class:`Event` instance of the interval.
    """
    def wrap(*args, **kwargs):
        # thread = getcurrent()
        args = list(args)
        stop_event = args[0]
        del args[0]
        args = tuple(args)
        while not stop_event.is_set():
            f(*args, **kwargs)
            stop_event.wait(time)
        host.detach_interval(thread_id)

    t2_stop = Event()
    args = list(args)
    args.insert(0, t2_stop)
    args = tuple(args)
    t = spawn(wrap, *args, **kwargs)
    thread_id = t
    host.attach_interval(thread_id, t2_stop)
    return t2_stop
