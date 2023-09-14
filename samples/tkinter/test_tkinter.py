import os
import sys
from tkinter import Button, Label, PhotoImage, TclVersion, Tk


def _test():
    root = Tk()
    text = (
        f"This is Tcl/Tk version {TclVersion}\n"
        "This should be a cedilla: \xe7"
    )
    label = Label(root, text=text)
    label.pack()
    test = Button(
        root,
        text="Click me!",
        command=lambda root=root: root.test.configure(
            text="[%s]" % root.test["text"]
        ),
    )
    # icon located in current directory is copied to "icon" folder when frozen
    # (see setup.py)
    icon_file = (
        os.path.join(os.path.dirname(sys.executable), "icon", "python.png")
        if getattr(sys, "frozen", False)
        else os.path.join(os.path.dirname(__file__), "logox128.png")
    )
    icon = PhotoImage(file=icon_file)
    root.tk.call("wm", "iconphoto", root._w, icon)
    test.pack()
    root.test = test
    quit = Button(root, text="QUIT", command=root.destroy)
    quit.pack()
    # The following three commands are needed so the window pops
    # up on top on Windows...
    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    _test()
