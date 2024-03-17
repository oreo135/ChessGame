from tkinter import *

root = Tk()  # create parent window


def volume_up():
    """output message to terminal to tell that the button is working"""
    print("Volume Increase +1")


# Create volume up button
vol_up = Button(root, text="+")
vol_up.pack()
root.mainloop()
