"""A simple Quote of the Day server."""

from __future__ import annotations

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol


class QOTD(Protocol):
    def connectionMade(self) -> None:
        self.transport.write(b"An apple a day keeps the doctor away\r\n")
        self.transport.loseConnection()


# Next lines are magic:
factory = Factory()
factory.protocol = QOTD

# 8007 is the port you want to run under. Choose something >1024
portNum = 8007
reactor.listenTCP(portNum, factory)
print("Listening on port", portNum)
reactor.run()
