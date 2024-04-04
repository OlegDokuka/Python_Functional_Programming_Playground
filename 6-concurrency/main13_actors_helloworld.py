# Example actors, similar to those described in the
# "In Depth Introduction to Thespian" document.
#
# Run this from the top level as:
#    $ python examples/hellogoodbye.py  [system-base-name]


import logging
from logsetup import logcfg
from datetime import timedelta
from thespian.actors import *
#
#                         -> World ->|
#                       /            |
# sender -> HelloActor /             |
#   ^                                |
#   |--------------------------------
class Hello(ActorTypeDispatcher):
    def receiveMsg_str(self, message, sender):
        logging.info('Hello got: %s', message)
        if message == 'are you there?':
            world = self.createActor(World)
            worldmsg = (sender, 'Hello,')
            self.send(world, worldmsg)

class World(ActorTypeDispatcher):
    def receiveMsg_tuple(self, message: tuple[ActorAddress, str], sender):
        logging.info('World got: %s', message)
        orig_sender, pre_world = message
        self.send(orig_sender, pre_world + ' world!')


class Goodbye(Actor):
    def receiveMessage(self, message, sender):
        self.send(sender, 'Goodbye')


def run_example(systembase=None):
    asys = ActorSystem(systembase, logDefs=logcfg)
    try:
        hello = ActorSystem().createActor(Hello)
        world = ActorSystem().createActor(World)
        goodbye = ActorSystem().createActor(Goodbye)
        greeting = ActorSystem().ask(world, (ActorSystem().systemAddress, "hello, "))
        print("-----------")
        print(greeting + '\n' + ActorSystem().ask(goodbye, None,
                                                  timedelta(milliseconds=100)))
    finally:
        ActorSystem().shutdown()

if __name__ == "__main__":
    import sys
    run_example(sys.argv[1] if len(sys.argv) > 1 else None)