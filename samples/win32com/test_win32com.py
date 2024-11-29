"""Implements _both_ a connectable client, and a connectable server.
https://brian3johnson.github.io/pywin32/com/samples/connect.html.

Note that we cheat just a little - the Server in this demo is not created
via Normal COM - this means we can avoid registering the server.
However, the server _is_ accessed as a COM object - just the creation
is cheated on - so this is still working as a fully-fledged server.
"""

from typing import ClassVar

import pythoncom
import win32com.server.connect
import win32com.server.util

# This is the IID of the Events interface both Client and Server support.
IID_IConnectDemoEvents = pythoncom.MakeIID(
    "{A4988850-49C3-11d0-AE5D-52342E000000}"
)


# The server which implements
# Create a connectable class, that has a single public method
# 'DoIt', which echos to a single sink 'DoneIt'
class ConnectableServer(win32com.server.connect.ConnectableServer):
    _public_methods_: ClassVar[list[str]] = [
        "DoIt",
        *win32com.server.connect.ConnectableServer._public_methods_,
    ]
    _connect_interfaces_: ClassVar = [IID_IConnectDemoEvents]

    # The single public method that the client can call on us
    # (ie, as a normal COM server, this exposes just this single method.
    def DoIt(self, arg) -> None:
        # Simply broadcast a notification.
        self._BroadcastNotify(self.NotifyDoneIt, (arg,))

    def NotifyDoneIt(self, interface, arg) -> None:
        interface.Invoke(1000, 0, pythoncom.DISPATCH_METHOD, 1, arg)


# Here is the client side of the connection world.
# Define a COM object which implements the methods defined by the
# IConnectDemoEvents interface.
class ConnectableClient:
    # This is another cheat - I _know_ the server defines the "DoneIt" event
    # as DISPID==1000 - I also know from the implementation details of COM
    # that the first method in _public_methods_ gets 1000.
    # Normally some explicit DISPID->Method mapping is required.
    _public_methods_: ClassVar = ["OnDoneIt"]

    def __init__(self) -> None:
        self.last_event_arg = None

    # A client must implement QI, and respond to a query for the Event interface.
    # In addition, it must provide a COM object (which server.util.wrap) does.
    def _query_interface_(self, iid):  # noqa: ANN202
        import win32com.server.util

        # Note that this seems like a necessary hack.  I am responding to
        # IID_IConnectDemoEvents but only creating an IDispatch gateway object.
        if iid == IID_IConnectDemoEvents:
            return win32com.server.util.wrap(self)
        return None

    # And here is our event method which gets called.
    def OnDoneIt(self, arg) -> None:
        self.last_event_arg = arg


def CheckEvent(server, client, val, verbose) -> None:
    client.last_event_arg = None
    server.DoIt(val)
    if client.last_event_arg != val:
        msg = f"Sent {val!r}, but got back {client.last_event_arg!r}"
        raise RuntimeError(msg)
    if verbose:
        print(f"Sent and received {val!r}")


# A simple test script for all this.
# In the real world, it is likely that the code controlling the server
# will be in the same class as that getting the notifications.
def test(verbose=0) -> None:
    import win32com.client.connect
    import win32com.client.dynamic
    import win32com.server.policy

    server = win32com.client.dynamic.Dispatch(
        win32com.server.util.wrap(ConnectableServer())
    )
    connection = win32com.client.connect.SimpleConnection()
    client = ConnectableClient()
    connection.Connect(server, client, IID_IConnectDemoEvents)
    CheckEvent(server, client, "Hello from cx_Freeze", verbose)
    CheckEvent(server, client, b"Here is a null>\x00<", verbose)
    CheckEvent(server, client, "Here is a null>\x00<", verbose)
    val = "test-\xe0\xf2"  # 2 extended characters.
    CheckEvent(server, client, val, verbose)
    if verbose:
        print("Everything seemed to work!")
    # Aggressive memory leak checking (ie, do nothing!) :-)
    # All should cleanup OK???


if __name__ == "__main__":
    test(1)
