import uuid
import pickle
import traceback
from urllib.parse import urlparse
from importlib import import_module

from .actor import Actor
from .channel import Channel
from ..util import FUTURE, ASK_RESPONSE, FUTURE_RESPONSE
from ..util import TYPE, METHOD, TELL, ASK, CHANNEL, FROM, TO, RPC_ID


class RPCDispatcher(Actor):
    """
    This is the actor that will manage remote sends and receives
    with other hosts. Each host has one, configured depending on
    the scheme specified when created.
    """

    def __init__(self, url, host, mode):
        self.server_model = import_module('pyactor.' + mode + 'server')
        self.url = url
        self.host = host
        aurl = urlparse(url)
        address = aurl.netloc.split(':')
        ip, port = address[0], address[1]
        self.source = self.server_model.Source((ip, int(port)))
        self.source.register_function(self.on_message)
        self.source.start()
        self.running = True
        self.channel = Channel()
        self.pending = {}  # Sent to another host
        self.executing = {}  # Waiting for the response in this server
        self.tell = ['stop']
        self.ask = []
        self.ask_ref = []
        self.tell_ref = []
        self.sinks = {}

    def get_sink(self, url):
        if url in self.sinks.keys():
            return self.sinks[url]
        else:
            self.sinks[url] = self.server_model.Sink(url)
            return self.sinks[url]

    def receive(self, msg):
        if msg[TYPE] == TELL and msg[METHOD] == 'stop':
            self.running = False
            self.source.stop()
        else:
            try:
                if msg[TYPE] == TELL:
                    self.get_sink(msg[TO]).send(msg)
                elif msg[TYPE] == ASK:
                    rpc_id = str(uuid.uuid4())
                    msg[RPC_ID] = rpc_id
                    self.pending[rpc_id] = msg[CHANNEL]
                    del msg[CHANNEL]
                    msg[FROM] = self.url
                    self.get_sink(msg[TO]).send(msg)
                elif msg[TYPE] == ASK_RESPONSE or msg[TYPE] == FUTURE_RESPONSE:
                    try:
                        if msg[RPC_ID] in self.executing.keys():
                            sink = self.get_sink(self.executing[msg[RPC_ID]])
                            sink.send(msg)
                            del self.executing[msg[RPC_ID]]
                    except TypeError as p:
                        print("Pickle ERR: impossible to marshall a return." +
                              " Returning a Proxy without the method in " +
                              f"_ref? {p}")
                    except Exception as e:
                        print(("Error sending a response to {!r}. "
                               .format(self.executing[msg[RPC_ID]])) + str(e))
                        del self.executing[msg[RPC_ID]]
                elif msg[TYPE] == FUTURE:
                    rpc_id = msg[RPC_ID]
                    self.pending[rpc_id] = msg[CHANNEL]
                    del msg[CHANNEL]
                    msg[FROM] = self.url
                    self.get_sink(msg[TO]).send(msg)
            except TypeError as p:
                print("Pickle ERROR: impossible to marshall a parameter." +
                      f"Passing a Proxy without the method in _ref? {p}")
            except Exception as e:
                print(e)

    def on_message(self, msg):
        try:
            msg = pickle.loads(msg.data)
            if msg[TYPE] == TELL:
                self.host.actors[msg[TO]].channel.send(msg)
            elif msg[TYPE] == ASK or msg[TYPE] == FUTURE:
                # Save rpc id and actor channel
                rpc_id = msg[RPC_ID]
                self.executing[rpc_id] = msg[FROM]
                # Change msg callback channel, add id
                msg[CHANNEL] = self.channel
                self.host.actors[msg[TO]].channel.send(msg)
            elif msg[TYPE] == ASK_RESPONSE or msg[TYPE] == FUTURE_RESPONSE:
                if msg[RPC_ID] in self.pending.keys():
                    self.pending[msg[RPC_ID]].send(msg)
                    del self.pending[msg[RPC_ID]]
        except KeyError as ke:
            print("ERROR: The actor", ke, "is offline.")
        except Exception as e:
            print(f"{self.url} :#: Connection ERROR: {e}")
            traceback.print_exc()
