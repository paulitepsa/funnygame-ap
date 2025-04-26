try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

from funnygame import Game
from apclient import APClient
import subprocess


class Launcher:
    def __init__(self):
        self.root = tk.Tk()
        self.HEIGHT = 150
        self.WIDTH = 300
        self.strDialogResult = ""
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        self.create_window()
        self.run()

    def run(self):

        self.root.mainloop()
        Game(self.strDialogResult)

    def create_window(self):
        self.root.width = self.WIDTH
        self.root.height = self.HEIGHT
        frame = tk.Frame(self.root, bg="#42c2f4")
        frame.place(relx=0.5, rely=0.02, relwidth=0.96, relheight=0.95, anchor="n")

        label_address = tk.Label(frame, font=40, text="Address")
        label_slotname = tk.Label(frame, font=40, text="Slot Name")
        label_password = tk.Label(frame, font=40, text="Password")

        entry_address = tk.Entry(frame, font=40)
        entry_slotname = tk.Entry(frame, font=40)
        entry_password = tk.Entry(frame, font=40)

        label_address.place(relwidth=0.4, relx=0.02, rely=0.02, relheight=0.20)
        label_slotname.place(relwidth=0.4, relx=0.02, rely=0.24, relheight=0.20)
        label_password.place(relwidth=0.4, relx=0.02, rely=0.46, relheight=0.20)

        entry_address.place(relwidth=0.5, relx=0.4, rely=0.02, relheight=0.20)
        entry_slotname.place(
            relwidth=0.5,
            relx=0.4,
            rely=0.24,
            relheight=0.20,
        )
        entry_password.place(
            relwidth=0.5,
            relx=0.4,
            rely=0.46,
            relheight=0.20,
        )
        entry_address.focus_set()

        # Here is the button call to the InputBox() function
        buttonInputBox = tk.Button(
            frame,
            text="OK",
            bg="#cccccc",
            font=60,
            command=lambda: self.dialog_result(
                [
                    entry_address.get().lower(),
                    entry_slotname.get(),
                    entry_password.get(),
                ]
            ),
        )
        buttonInputBox.place(relx=0.05, rely=0.8, relwidth=0.90, relheight=0.2)

    def dialog_result(self, result):

        self.strDialogResult = result
        # This line quits from the dialog

        self.root.quit()


# Launch ...
if __name__ == "__main__":
    app = Launcher()
