# Service sample with asyncio

This is the same as the "service" sample, but with asyncio
support. The ProactorEventLoop must be created in the service
handler's __init__ method, because it's the only one which is
guaranteed to be called from the main interpreter thread.
