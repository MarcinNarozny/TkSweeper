import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import os

#test version

class GameWindow:

    def __init__(self, window, setup_values):
        self.game_frame = tk.Frame(window)
        self.game_frame.pack(anchor='nw')
        self.first_click = True
        self.height = setup_values[0]
        self.width = setup_values[1]      
        self.bombs = setup_values[2]
        self.draw_window(self.width, self.height)
        self.read_assets()
    

    def draw_window(self, width, height):
        self.minefield = []
        for x in range(height):
            row=[]
            for y in range(width):
                row.append(tk.Button(self.game_frame,))
                row[-1].bind('<Button-1>', self.field_click)
                row[-1].grid(row=x, column=y)
            self.minefield.append(row)
        
    
    def field_click(self,event):
        button = event.widget
        print(type(button))
        if self.first_click == True:
            self.first_click = False
            self.neighbours_map = self.generate_neighbours(self.generate_bombs(self.bombs))
        
        result = self.field_reveal(button)
        if result == 'bomb':
            for row in self.minefield:
                for left_button in row:
                    self.field_reveal(left_button)
        

    def generate_bombs(self, bombs_amount):
        bomb_indicies = np.random.choice(self.width*self.height, size=bombs_amount, replace=False)
        bomb_indicies  = np.unravel_index(bomb_indicies , (self.height, self.width))
        bomb_indicies  = list(zip(*bomb_indicies ))
        print(bomb_indicies)
        return bomb_indicies
    

    def generate_neighbours(self, bomb_indicies):
        neighbours_map=[]
        for _ in range(self.height):
            neighbours_map.append([0]*self.width)
        
        for bomb_x,bomb_y in bomb_indicies:
            neighbours_map[bomb_x][bomb_y] = "bomb"
            for y in range(max(0, bomb_y-1), min(self.width, bomb_y+2)):
                for x in range(max(0, bomb_x-1), min(self.height, bomb_x+2)):
                    if type(neighbours_map[x][y]) == int:
                        neighbours_map[x][y] += 1
        neighbours_map = [[str(x) for x in row] for row in neighbours_map]
        print(neighbours_map)
        return neighbours_map


    def field_reveal(self,button):
        grid_info = button.grid_info()
        button_x, button_y = grid_info['row'],grid_info['column']
        image = self.neighbours_map[button_x][button_y]
        if image != '0':
            button.configure(image=self.assets[self.neighbours_map[button_x][button_y]])
        return image
            

    def read_assets(self):
        self.assets={}
        assets_path='assets/'
        assets_contents=[file for file in os.listdir(assets_path)]
        for file_name in assets_contents:
            image_path = os.path.join(assets_path,file_name)
            image = Image.open(image_path)
            image = image.resize((22,25))
            image = ImageTk.PhotoImage(image)
            self.assets[file_name.split('.')[0]] = image
        