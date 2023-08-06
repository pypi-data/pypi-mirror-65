import inspect
from os import path
from signal import SIGINT
from importlib import import_module

from urllib.parse import urlparse
from .proxy import Proxy, set_actor, ProxyRef, TellWrapper
from .exceptions import HostDownError, AlreadyExistsError, NotFoundError, \
    HostError, IntervalError
from . import util

# import pyactor.thread.parallels
# parallels = pyactor.thread.parallels
core_type = None
available_types = ['thread', 'green_thread']
actor_module = None
intervals = None
parallels = None
future = None
rpcactor = None
signal = None


def set_rabbit_credentials(user, password):
    """
    If you use a RabbitMQ server and want to make remote queries, you might
    need to specify new credentials for connection.

    By default, PyActor uses the guest RabbitMQ user.

    :param str. user: Name for the RabbitMQ user.
    :param str. password: Password for the RabbitMQ user.
    """
    util.RABBIT_USER = user
    util.RABBIT_PASS = password


def set_context(module_name='thread'):
    """
    This function initializes the execution context deciding which
    type of threads are being used: classic python threads or green
    threads, provided by Gevent.

    This should be called first of all in every execution, otherwise,
    the library would not work.

    The default module is 'thread'.

    :param str. module_name: Name of the module you want to use
        ('thread' or 'green_thread').
    """
    global core_type
    if core_type is None and module_name in available_types:
        core_type = module_name
        util.core_type = core_type
        global actor_module
        actor_module = import_module('pyactor.' + module_name + '.actor')
        global intervals
        intervals = import_module('pyactor.' + module_name + '.intervals')
        global parallels
        parallels = import_module('pyactor.' + module_name + '.parallels')
        global future
        future = import_module('pyactor.' + module_name + '.future')
        set_actor(module_name)
        global rpcactor
        rpcactor = import_module('pyactor.' + module_name + '.rpcactor')
        global signal
        if module_name == 'green_thread':
            signal = import_module('gevent')
        else:
            signal = import_module('signal')
    else:
        if core_type is not None:
            raise Exception("The core type was previously configured.")
        raise Exception("Bad core type.")


def create_host(url="local://local:6666/host"):
    """
    This is the main function to create a new Host to which you can
    spawn actors. It will be set by default at local address if no
    parameter *url* is given. This function should be called once
    for execution or after calling :meth:`~.shutdown` to the previous
    host.

    However, it is possible to create locally more than one host
    and simulate a remote communication between them if they are of some
    remote type (`http` or `amqp`), but the first one created will
    be the main host, which is the one hosting the queries from
    the main function.
    Of course, every host must be initialized with a different URL(port).
    Although that, more than one host should not be required for any real
    project.

    :param str. url: URL where to start and bind the host.
    :return: :class:`~.Proxy` to the new host created.
    :raises: Exception if there is a host already created with that URL.
    """
    if url in util.hosts.keys():
        raise HostError("Host already created. Only one host can"
                        " be ran with the same url.")
    else:
        if not util.hosts:
            util.main_host = Host(url)
            util.hosts[url] = util.main_host
        else:
            util.hosts[url] = Host(url)
        return util.hosts[url].proxy


class Host(object):
    """
    Host must be created using the function :func:`~create_host`.
    Do not create a Host directly.

    Host is a container for actors. It manages the spawn and
    elimination of actors and their communication through channels. Also
    configures the remote points where the actors will be able to receive
    and send queries remotely. Additionally, controls the correct management
    of its actors' threads and intervals.

    The host is managed as an actor itself so you interact with it through
    its :class:`~.Proxy`. This allows you to pass it to another host to
    spawn remotely.

    :param str. url: URL that identifies the host and where to find it.
    """
    _tell = {'attach_interval', 'detach_interval', 'hello', 'stop_actor'}
    _ask = {'spawn', 'lookup', 'lookup_url', 'say_hello', 'has_actor'}
    _ref = {'spawn', 'lookup', 'lookup_url'}

    def __init__(self, url):
        self.actors = {}
        self.threads = {}
        self.pthreads = {}
        self.intervals = {}
        self.locks = {}
        self.url = url
        self.running = False
        self.alive = True
        self.__load_transport(url)
        self.__init_host()

        self.ppool = None
        # self.cleaner = interval_host(get_host(), CLEAN_INT, self.do_clean)

    def hello(self):
        print("Hello!!")

    def say_hello(self):
        print("Sending hello.")
        return "Hello from HOST!!"

    def __load_transport(self, url):
        """
        For remote communication. Sets this host's communication dispatcher
        at the address and port specified.

        The scheme must be 'http' if using a XMLRPC dispatcher.
        'amqp' for RabbitMQ communications.

        This method is internal. Automatically called when creating the host.

        :param str. url: URL where to bind the host. Must be provided in
            the typical form: 'scheme://address:port/hierarchical_path'
        """
        aurl = urlparse(url)
        addrl = aurl.netloc.split(':')
        self.addr = addrl[0], addrl[1]
        self.transport = aurl.scheme
        self.host_url = aurl

        if aurl.scheme == 'http':
            self.__launch_actor('http',
                                rpcactor.RPCDispatcher(url, self, 'rpc'))

        elif aurl.scheme == 'amqp':
            self.__launch_actor('amqp', rpcactor.RPCDispatcher(url, self,
                                                               'rabbit'))

    def spawn(self, aid, klass, *param, **kparam):
        """
        This method creates an actor attached to this host. It will be
        an instance of the class *klass* and it will be assigned an ID
        that identifies it among the host.

        This method can be called remotely synchronously.

        :param str. aid: identifier for the spawning actor. Unique within
            the host.
        :param class klass: class type of the spawning actor. If you are
            spawning remotely and the class is not in the server module,
            you must specify here the path to that class in the form
            'module.py/Class' so the server can import the class and create
            the instance.
        :param param: arguments for the init function of the
            spawning actor class.
        :param kparam: arguments for the init function of the
            spawning actor class.
        :return: :class:`~.Proxy` to the spawned actor.
        :raises: :class:`AlreadyExistsError`, if the ID specified is
            already in use.
        :raises: :class:`HostDownError` if the host is not initiated.
        """
        if param is None:
            param = []
        if not self.alive:
            raise HostDownError()
        if isinstance(klass, str):
            module, klass = klass.split('/')
            module_ = __import__(module, globals(), locals(),
                                 [klass])
            klass_ = getattr(module_, klass)
        elif isinstance(klass, type):
            klass_ = klass
        else:
            raise Exception(f"Given class is not a class: {klass}")
        url = f'{self.transport}://{self.host_url.netloc}/{aid}'
        if url in self.actors.keys():
            raise AlreadyExistsError(url)
        else:
            obj = klass_(*param, **kparam)
            obj.id = aid
            obj.url = url
            if self.running:
                obj.host = self.proxy
            # else:
            #     obj.host = Exception("Host is not an active actor. \
            #                           Use 'init_host' to make it alive.")

            if hasattr(klass_, '_parallel') and klass_._parallel:
                new_actor = parallels.ActorParallel(url, klass_, obj)
                lock = new_actor.get_lock()
                self.locks[url] = lock
            else:
                new_actor = actor_module.Actor(url, klass_, obj)

            obj.proxy = Proxy(new_actor)
            self.__launch_actor(url, new_actor)
            return Proxy(new_actor)

    def has_actor(self, aid):
        """
        Checks if the given id is used in the host by some actor.

        :param str. aid: identifier of the actor to check.
        :return: True if the id is used within the host.
        """
        url = f'{self.transport}://{self.host_url.netloc}/{aid}'
        return url in self.actors.keys()

    def lookup(self, aid):
        """
        Gets a new proxy that references to the actor of this host
        (only actors in this host) identified by the given ID.

        This method can be called remotely synchronously.

        :param str. aid: identifier of the actor you want.
        :return: :class:`~.Proxy` to the actor required.
        :raises: :class:`NotFoundError` if the actor does not exist.
        :raises: :class:`HostDownError` if the host is down.
        """
        if not self.alive:
            raise HostDownError()
        url = f"{self.transport}://{self.host_url.netloc}/{aid}"
        if url in self.actors.keys():
            return Proxy(self.actors[url])
        else:
            raise NotFoundError(url)

    def shutdown(self):
        # """
        # For internal calls.
        # """
        if self.alive:
            print(f"Host {self.addr} :#: shutting down...")
            for interval_event in self.intervals.values():
                interval_event.set()

            for actor in self.actors.values():
                Proxy(actor).stop()

            # stop the pool (close & join)
            if self.ppool is not None:
                if core_type == 'thread':
                    self.ppool.close()
                self.ppool.join()

            # By now, all pthreads should be gone
            for parallel in self.pthreads.keys():
                parallel.join()

            for thread in self.threads.keys():
                try:
                    thread.join()
                except Exception as e:
                    print(e)

            self.locks.clear()
            self.actors.clear()
            self.threads.clear()
            self.pthreads.clear()
            self.running = False
            self.alive = False

            del util.hosts[self.url]
            if util.main_host.url == self.url:
                util.main_host = (list(util.hosts.values())[0]
                                  if util.hosts.values() else None)

            print(f"Host {self.addr} :#: Bye!")

    def stop_actor(self, aid):
        """
        This method removes one actor from the Host, stopping it and deleting
        all its references.

        :param str. aid: identifier of the actor you want to stop.
        """
        url = f"{self.transport}://{self.host_url.netloc}/{aid}"
        if url != self.url:
            a = self.actors[url]
            Proxy(a).stop()
            a.thread.join()
            del self.actors[url]
            del self.threads[a.thread]

    def lookup_url(self, url, klass, module=None):
        """
        Gets a proxy reference to the actor indicated by the URL in the
        parameters. It can be a local reference or a remote direction to
        another host.

        This method can be called remotely synchronously.

        :param srt. url: address that identifies an actor.
        :param class klass: the class of the actor.
        :param srt. module: if the actor class is not in the calling module,
            you need to specify the module where it is here. Also, the *klass*
            parameter change to be a string.
        :return: :class:`~.Proxy` of the actor requested.
        :raises: :class:`NotFoundError`, if the URL specified do not
            correspond to any actor in the host.
        :raises: :class:`HostDownError`  if the host is down.
        :raises: :class:`HostError`  if there is an error looking for
            the actor in another server.
        """
        if not self.alive:
            raise HostDownError()
        aurl = urlparse(url)
        if self.__is_local(aurl):
            if url not in self.actors.keys():
                raise NotFoundError(url)
            else:
                return Proxy(self.actors[url])
        else:
            try:
                dispatcher = self.actors[aurl.scheme]
                if module is not None:
                    try:
                        module_ = __import__(module, globals(), locals(),
                                             [klass])
                        klass_ = getattr(module_, klass)
                    except Exception as e:
                        raise HostError("At lookup_url: " +
                                        "Import failed for module " + module +
                                        ", class " + klass +
                                        ". Check this values for the lookup." +
                                        " ERROR: " + str(e))
                elif inspect.isclass(klass):
                    klass_ = klass
                else:
                    raise HostError("The class specified to look up is" +
                                    " not a class.")
                remote_actor = actor_module.ActorRef(url, klass_,
                                                     dispatcher.channel)
                return Proxy(remote_actor)
            except HostError:
                raise
            except Exception as e:
                raise HostError(
                    f"ERROR looking for the actor on another server. Hosts must"
                    f" be in http to work properly. {str(e)}")

    def __is_local(self, aurl):
        # '''Private method.
        # Tells if the address given is from this host.
        #
        # :param ParseResult aurl: address to analyze.
        # :return: (*Bool.*) If is local (**True**) or not (**False**).
        # '''
        return self.host_url.netloc == aurl.netloc

    def __launch_actor(self, url, actor):
        # '''Private method.
        # This function makes an actor alive to start processing queries.
        #
        # :param str. url: identifier of the actor.
        # :param Actor actor: instance of the actor.
        # '''
        actor.run()
        self.actors[url] = actor
        self.threads[actor.thread] = url

    def __init_host(self):
        # '''
        # This method creates an actor for the Host so it can spawn actors
        # remotely. Called always from the init function of the host, so
        # no need for calling this directly.
        # '''
        if not self.running and self.alive:
            self.id = self.url
            host = actor_module.Actor(self.url, Host, self)
            self.proxy = Proxy(host)
            # self.actors[self.url] = host
            self.__launch_actor(self.url, host)
            # host.run()
            # self.threads[host.thread] = self.url
            self.running = True

    def attach_interval(self, interval_id, interval_event):
        """Registers an interval event to the host."""
        self.intervals[interval_id] = interval_event

    def detach_interval(self, interval_id):
        """Deletes an interval event from the host registry."""
        del self.intervals[interval_id]

    def dumps(self, param):
        """
        Checks the parameters generating new proxy instances to avoid
        query concurrences from shared proxies and creating proxies for
        actors from another host.
        """
        if isinstance(param, Proxy):
            module_name = param.actor.klass.__module__
            if module_name == '__main__':
                module_name = path.splitext(
                    path.basename(inspect.getfile(param.actor.klass)))[0]
            return ProxyRef(param.actor.url, param.actor.klass.__name__,
                            module_name)
        elif isinstance(param, list):
            return [self.dumps(elem) for elem in param]
        elif isinstance(param, dict):
            new_dict = param
            for key in new_dict.keys():
                new_dict[key] = self.dumps(new_dict[key])
            return new_dict
        elif isinstance(param, tuple):
            return tuple([self.dumps(elem) for elem in param])
        else:
            return param

    def loads(self, param):
        """
        Checks the return parameters generating new proxy instances to
        avoid query concurrences from shared proxies and creating
        proxies for actors from another host.
        """
        if isinstance(param, ProxyRef):
            try:
                return self.lookup_url(param.url, param.klass, param.module)
            except HostError:
                print("Can't lookup for the actor received with the call.",
                      "It does not exist or the url is unreachable.",
                      param)
                raise HostError(param)
        elif isinstance(param, list):
            return [self.loads(elem) for elem in param]
        elif isinstance(param, tuple):
            return tuple([self.loads(elem) for elem in param])
        elif isinstance(param, dict):
            new_dict = param
            for key in new_dict.keys():
                new_dict[key] = self.loads(new_dict[key])
            return new_dict
        else:
            return param

    def new_parallel(self, a_function, *params):
        """
        Register a new thread executing a parallel method.
        """
        # Create a pool if not created (threads or Gevent...)
        if self.ppool is None:
            if core_type == 'thread':
                from multiprocessing.pool import ThreadPool
                self.ppool = ThreadPool(500)
            else:
                from gevent.pool import Pool
                self.ppool = Pool(500)
        # Add the new task to the pool
        self.ppool.apply_async(a_function, *params)


def shutdown(url=None):
    """
    Stops the Host passed by parameter or all of them if none is
    specified, stopping at the same time all its actors.
    Should be called at the end of its usage, to finish correctly
    all the connections and threads.
    """
    if url is None:
        for host in list(util.hosts.values()):
            host.shutdown()
        global core_type
        core_type = None
    else:
        host = util.hosts[url]
        host.shutdown()


def signal_handler(signal=None, frame=None):
    # '''
    # This gets the signal of Ctrl+C and stops the host. It also ends
    # the execution. Needs the invocation of :meth:`serve_forever`.
    #
    # :param signal: SIGINT signal interruption sent with a Ctrl+C.
    # :param frame: the current stack frame. (not used)
    # '''
    print("You pressed Ctrl+C!")
    util.main_host.serving = False
    shutdown(util.main_host.url)


def serve_forever():
    """
    This allows the host (main host) to keep alive indefinitely so its actors
    can receive queries at any time.
    The main thread stays blocked forever.
    To kill the execution, press Ctrl+C.

    See usage example in :ref:`sample6`.
    """
    if not util.main_host.alive:
        raise Exception("This host is already shut down.")
    util.main_host.serving = True
    signal.signal(SIGINT, signal_handler)
    print("Press Ctrl+C to kill the execution")
    while util.main_host is not None and util.main_host.serving:
        try:
            sleep(1)
        except Exception:
            pass
    print("BYE!")


def interval(host, time, actor, method, *args, **kwargs):
    """
    Creates an Event attached to the host for management that will
    execute the *method* of the *actor* every *time* seconds.

    See example in :ref:`sample_inter`

    :rtype:
    :param Proxy host: host that will manage the interval, commonly the
        host of the actor.
    :param float time: seconds for the intervals.
    :param Proxy actor: actor to which make the call every *time* seconds.
    :param Str. method: method of the *actor* to be called.
    :param list args: arguments for *method*.
    :return: :class:`Event` instance of the interval.
    """
    call = getattr(actor, method, None)
    if not callable(call):
        raise IntervalError(
            f"The actor {actor.get_id()} does not have the method {method}.")
    if call.__class__.__name__ in ["TellWrapper", "TellRefWrapper"]:
        # If the method is a normal tell, the interval thread can send
        # the calls normally.
        # It it is a Ref Tell, the proxies in the args would be parsed
        # during the call to this very method. So the call can be made
        # as a normal Tell. The actor will do the loads normally on the
        # receive as it has its methods marked as ref.
        if call.__class__.__name__ is "TellRefWrapper":
            call.__call__ = TellWrapper.__call__

        return intervals.interval_host(host, time, call, *args, **kwargs)
    else:
        raise IntervalError("The callable for the interval must be a tell" +
                            " method of the actor.")


def later(timeout, actor, method, *args, **kwargs):
    """
    Sets a timer that will call the *method* of the *actor* past *timeout*
    seconds.

    See example in :ref:`sample_inter`

    :param int timeout: seconds until the method is called.
    :param Proxy actor: actor to which make the call after *time* seconds.
    :param Str. method: method of the *actor* to be called.
    :param list args: arguments for *method*.
    :return: manager of the later (Timer in thread,
        Greenlet in green_thread)
    """
    call = getattr(actor, method, None)
    if not callable(call):
        raise IntervalError(f"later: The actor {actor.get_id()} does not "
                            f"have the method {method}.")
    if call.__class__.__name__ in ["TellWrapper", "TellRefWrapper"]:
        # As with the interval, args have already been dumped.
        if call.__class__.__name__ is "TellRefWrapper":
            call.__call__ = TellWrapper.__call__
        return intervals.later(timeout, call, *args, **kwargs)
    else:
        raise IntervalError("The callable for the later must be a tell "
                            "method of the actor.")


def sleep(seconds):
    """
    Facade for the sleep function. Do not use time.sleep if you are
    running green threads.
    """
    intervals.sleep(seconds)
