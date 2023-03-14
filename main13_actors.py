from thespian.actors import *

class Hello(Actor):
    def receiveMessage(self, message, sender):
        self.send(sender, 'Hello, World!')


def main():
    # Schedule three calls *concurrently*:
    hello = ActorSystem().createActor(Hello)
    print(ActorSystem().ask(hello, 'hi', 1))
    ActorSystem().tell(hello, ActorExitRequest())


if __name__ == '__main__':
    main()
