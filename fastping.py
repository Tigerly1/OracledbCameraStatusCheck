from tkinter import *
import subprocess
import sys


class App(Frame):

    def __init__(self, okno=None):
        Frame.__init__(self, okno)
        self.okno = okno
        self.init_window()

    def init_window(self):
        self.okno.title("Fast ping checker")
        self.okno.minsize(width=1000, height=800)
        self.okno.maxsize(width=1000, height=800)
        self.pack(fill=BOTH, expand=1)
        quitbutton = Button(self, text="Exit", height=5, width=25, command=self.client_exit, fg='black',
                            bg='white', activeforeground='white', activebackground='black', bd='3')
        startbutton = Button(self, text="Start",height=5, width=25, command=self.client_start_ping, fg='black',
                            bg='white', activeforeground='white', activebackground='black', bd='3')
        quitbutton.place(x=800, y=700)
        startbutton.place(x=15, y=700)

    def client_exit(self):
        sys.exit()

    def client_start_ping(self):
        var = StringVar()
        label = Message(root, textvariable=var, relief=RAISED)
        label.config(width=666)
        label.place(x=15, y=1)
        output = subprocess.check_output("python fst.py")
        var.set(output)


root = Tk()
app = App(root)
root.mainloop()





