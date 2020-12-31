from tkinter import Tk, Label, Button, BOTTOM

root = Tk()
root.title("Button")
Label(text="I am a button").pack(pady=15)
Button(text="Button").pack(side=BOTTOM)
root.mainloop()
