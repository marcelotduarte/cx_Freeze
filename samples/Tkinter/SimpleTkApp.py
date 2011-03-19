try:
    from tkinter import *
except ImportError:
    from Tkinter import *

root = Tk()
root.title('Button')
Label(text='I am a button').pack(pady=15)
Button( text='Button') .pack(side=BOTTOM)
root.mainloop()

