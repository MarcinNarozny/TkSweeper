import tkinter as tk
from game import GameWindow

modes = {
    'easy': (9,9,10),
    'medium': (16,16,40),
    'hard': (16,30,99)
}


class Menu(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master, height=100, width=150)     
        for mode in modes.keys():
            tk.Button(self, text=mode, width=10,
                      command = lambda m=modes[mode]: self.display_minefield(m)).pack()

    def display_minefield(self, mode):
        rows = mode[0]
        columns = mode[1]
        bombs = mode[2]
        GameWindow(self.master, rows, columns, bombs).grid(row=0, column=0, sticky="nsew")