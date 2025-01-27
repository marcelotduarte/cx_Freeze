import os
import sys
from tkinter import Button, Label, PhotoImage, TclVersion, Tk


def _test() -> None:
    root = Tk()
    text = (
        f"This is Tcl/Tk version {TclVersion}\nThis should be a cedilla: \xe7"
    )
    label = Label(root, text=text)
    label.pack()
    test_button = Button(
        root,
        text="Click me!",
        command=lambda root=root: root.test.configure(
            text=f"[{root.test['text']}]"
        ),
    )
    # icon located in current directory is copied to "share" folder when frozen
    # (see setup.py)
    icon_file = (
        os.path.join(os.path.dirname(sys.executable), "share", "python.png")
        if getattr(sys, "frozen", False)
        else os.path.join(os.path.dirname(__file__), "logox128.png")
    )
    icon = PhotoImage(file=icon_file)
    root.tk.call("wm", "iconphoto", root._w, icon)  # noqa: SLF001
    test_button.pack()
    root.test = test_button
    quit_button = Button(root, text="QUIT", command=root.destroy)
    quit_button.pack()
    # The following three commands are needed so the window pops
    # up on top on Windows...
    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    _test()
