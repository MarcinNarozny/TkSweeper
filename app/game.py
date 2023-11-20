import tkinter as tk
import os
import random


class GameWindow(tk.Frame):
    def __init__(self, master, rows, columns, bombs):
        super().__init__(master)
        minefield = Minefield(self, rows, columns, bombs)
        minefield.grid(row=1, column=0)
        self.controls = Controls(self, minefield)
        self.controls.grid(row=0, column=0)
        self.set_button_image("playing")
        self.tkraise()

    def set_button_image(self, name):
        self.controls.reset_button.configure(image=self.controls.icons[name])


class Controls(tk.Frame):
    def __init__(self, master, minefield):
        super().__init__(master)
        self.reset_button = tk.Button(self, anchor="center", command=minefield.reset)
        self.reset_button.pack(side='top')
        self.load_icons()

    def load_icons(self):
        self.icons = {}
        icons_folder = 'app/sun/'
        icon_names = [icon for icon in os.listdir(icons_folder)]
        for icon_name in icon_names:
            img = tk.PhotoImage(file=os.path.join(icons_folder,icon_name))
            self.icons[icon_name.split('.')[0]] = img


class Minefield(tk.Frame):
    def __init__(self, master, rows, columns, bombs):
        super().__init__(master)
        self.rows = rows
        self.columns = columns
        self.bombs = bombs
        self.game_over = False
        self.board = []
        self.load_icons()
        for row in range(rows):
            board_row = []
            for column in range(columns):
                field = self.Field(self, row=row, col=column)
                field.grid(row=row, column=column)
                board_row.append(field)
            self.board.append(board_row)
        self.grid(row=0, column=0, sticky="nsew")
        
    def load_icons(self):
        self.icons = {}
        icons_folder = 'app/icons/'
        icon_names = [icon for icon in os.listdir(icons_folder)]
        for icon_name in icon_names:
            img = tk.PhotoImage(file=os.path.join(icons_folder,icon_name))
            self.icons[icon_name.split('.')[0]] = img

    class Field(tk.Button):

        first_click = True

        fields_revealed = 0

        def __init__(self, master, col, row):
            self.master = master
            super().__init__(master, image=self.master.icons["empty"])
            self.col = col
            self.row = row
            self.value = 0
            self.status = 'hidden'
            self.bind('<Button-1>', self.left_click)
            self.bind('<Button-3>', self.right_click)

        def left_click(self, event):

            if self.__class__.first_click:
                self.master.assign_bombs(self, event.num)

            if not self.master.game_over:
                if self.status == "hidden":
                        self.master.field_reveal(self)
                elif self.status == "revealed":
                    self.master.reveal_if_nearby_flags_ready(self)
            
        def right_click(self, event):

            if self.__class__.first_click:
                self.master.assign_bombs(self, event.num)

            if not self.master.game_over:
                if self.status == 'hidden':
                    self.configure(image=self.master.icons["flag"])
                    self.status = 'flag'
                elif self.status == 'flag':
                    self.configure(image=self.master.icons["empty"])
                    self.status = 'hidden'
                elif self.status == "revealed":
                    self.master.reveal_if_nearby_flags_ready(self)

    def iterate_over_neighbours(self, field, command):
        min_row = max(0, field.row - 1)
        max_row = min(len(self.board), field.row + 2)
        min_col = max(0, field.col - 1)
        max_col = min(len(self.board[0]), field.col + 2)
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                if (row, col) != (field.row, field.col):
                    command(self.board[row][col])

    def field_reveal(self, field):
        if field.status == "hidden":
            field.configure(image=self.icons[str(field.value)])
            field.status = 'revealed'
            self.Field.fields_revealed +=1
            if self.Field.fields_revealed == (self.rows * self.columns) - self.bombs:
                self.master.set_button_image("won")
                self.end_game()
            if field.value == "bomb":
                self.master.set_button_image("lost")
                self.end_game()
            elif field.value == 0:
                self.iterate_over_neighbours(field, self.field_reveal)

    def flags_nearby(self, field):
        flags = 0
        def count_flag(field):
            if field.status == "flag":
                nonlocal flags
                flags += 1
        self.iterate_over_neighbours(field, count_flag)
        return flags
    
    def reveal_if_nearby_flags_ready(self, field):
        if self.flags_nearby(field) >= field.value and field.status == "revealed":
            self.iterate_over_neighbours(field, self.field_reveal)

    def assign_bombs(self, field, mouse_button):
        def assign_bomb_neighbours(field):
            if type(field.value) == int:
                field.value +=1
    
        self.Field.first_click = False
        viable_bomb_cords = [(row,col) for col in range(self.columns) for row in range(self.rows)]
        if mouse_button == 1:
            viable_bomb_cords = [cords for cords in viable_bomb_cords if cords != (field.row,field.col)]
        bomb_cords = random.sample(viable_bomb_cords, self.bombs)
        fields_with_bombs = [self.board[row][col] for (row,col) in bomb_cords]
        for field in fields_with_bombs:
            field.value = "bomb"
            self.iterate_over_neighbours(field, assign_bomb_neighbours)

    def end_game(self):
        self.game_over = True
        for row in self.board:
            for field in row:
                if field.status != "flag":    
                    field.configure(image=self.icons[str(field.value)])

    def reset(self):
        for row in self.board:
            for field in row:
                field.value = 0
                field.status = 'hidden'
                field.configure(image=self.icons["empty"])
        self.Field.first_click = True
        self.Field.fields_revealed = 0
        self.game_over = False
        self.master.set_button_image("playing")