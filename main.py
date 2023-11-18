import tkinter as tk
from menu import Menu


def main():
    window = tk.Tk()
    window.resizable(0,0)
    window_container = tk.Frame(window)
    window_container.pack()
    window.title('TkSweeper')
    menu = Menu(window_container)
    menu.grid(row=0, column=0, sticky="nsew")
    window.mainloop()

if __name__ == "__main__":
    main()
