print("Hi, I'm a package!")

raise Exception("This package-level exception should not occur during freeze")

from . import dummymodule
