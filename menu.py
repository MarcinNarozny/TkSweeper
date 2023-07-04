import tkinter as tk
from game import GameWindow
    #height,width,bombs
Modes = {
    'easy': (10,10,10),
    'medium': (16,16,40),
    'hard': (16,30,99)
}

class MainMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack()
        #self.window.geometry('250x350')
        self.window.title('Minesweeper')
        self.create_buttons()


    def set_mode(self, setup):
        self.menu_frame.pack_forget()
        self.gamewindow=GameWindow(self.window, setup)


    def create_buttons(self):
        easy_mode = tk.Button(self.menu_frame, text='easy', width=10, command = lambda : self.set_mode(Modes['easy']))
        easy_mode.pack()
        medium_mode = tk.Button(self.menu_frame, text='medium', width=10, command = lambda : self.set_mode(Modes['medium']))
        medium_mode.pack()
        hard_mode = tk.Button(self.menu_frame, text='hard', width=10, command = lambda : self.set_mode(Modes['hard']))
        hard_mode.pack()