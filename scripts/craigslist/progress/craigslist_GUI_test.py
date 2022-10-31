import sys
import os
from tkinter import Tk, Label, Button

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

root = Tk()

Label(root, text="Hello World!").pack()
Button(root, text="Restart", command=restart_program).pack()

root.mainloop()


# import sys
# import os

# def restart_program():
#     """Restarts the current program.
#     Note: this function does not return. Any cleanup action (like
#     saving data) must be done before calling this function."""
#     python = sys.executable
#     os.execl(python, python, * sys.argv)

# if __name__ == "__main__":
#     answer = raw_input("Do you want to restart this program ? ")
#     if answer.lower().strip() in "y yes".split():
#         restart_program()