import tkinter as tk
import numpy as np
import os

#test version

class GameWindow:

    def __init__(self, window, setup_values):
        self.game_window_frame = tk.Frame(window)
        self.minefield_frame = tk.Frame(self.game_window_frame)
        window.withdraw()
        self.game_window_frame.pack() #anchor='nw'
        self.first_click_ever = True
        self.height = setup_values[0]
        self.width = setup_values[1]      
        self.bombs = setup_values[2]
        self.fields_revealed = 0
        self.read_assets()
        self.draw_window(self.width, self.height)
        self.minefield_frame.pack()
        self.game_window_frame.pack()
        window.deiconify()
        window.update()


    def reset(self):
        for y in range(self.height):
            for x in range(self.width):    
                self.minefield[y][x].configure(image=self.assets['empty'])
        self.first_click_ever = True
        
    def draw_window(self, width, height):
        self.minefield = []
              
        for y in range(height):
            row=[]
            for x in range(width):    
                button = tk.Button(self.minefield_frame,  image=self.assets['empty']) #compound="center",anchor="center",
                button.bind('<Button-1>', self.left_click)
                button.bind('<Button-3>', self.right_click)          
                button.grid(row=y, column=x)
                row.append(button)
            self.minefield.append(row)
        
        reset_button = tk.Button(self.game_window_frame, compound="center", anchor="center", command=self.reset)
        reset_button.pack(side='top')
        
    
    def first_click(self,button, left_or_right):
        if self.first_click_ever == True:
            self.fields_revealed = 0
            self.first_click_ever = False
            self.neighbours_map = self.generate_neighbours(self.generate_bombs(self.bombs, button,left_or_right))


    def left_click(self,event):  
        button = event.widget

        #if str(button.cget('image')) == str(self.assets['empty']):
            
        self.first_click(button, True)
        result = self.field_reveal(button)
        if result == 'bomb':
            self.reveal_all()
            print('YOU LOST :(')
        if self.fields_revealed == self.height*self.width-self.bombs:
            self.reveal_all()
            print('YOU WON :)')


    def right_click(self,event):
        button = event.widget
        if str(button.cget('image')) == str(self.assets['empty']):
            button.configure(image=self.assets['flag'])
        elif str(button.cget('image')) == str(self.assets['flag']):
            button.configure(image=self.assets['empty'])
        self.first_click(button, False)
        pass


    def generate_bombs(self, bombs_amount, button, left_click):
        if left_click:
            button_y, button_x = self.button_coordinates(button)
            possible_bomb_coordinates = list(range(self.width*self.height))
            possible_bomb_coordinates.pop(button_y*self.width+button_x)
        else:
            possible_bomb_coordinates = self.height*self.width

        bomb_indicies = np.random.choice(possible_bomb_coordinates, size=bombs_amount, replace=False)
        bomb_indicies  = np.unravel_index(bomb_indicies , (self.height, self.width))
        bomb_indicies  = list(zip(*bomb_indicies))
        return bomb_indicies
    

    def iterate_over_neighbours(self,y_limiter,x_limiter,function):
        for y in range(max(0, y_limiter-1), min(self.height, y_limiter+2)):
            for x in range(max(0, x_limiter-1), min(self.width, x_limiter+2)):
                function(y,x)


    def generate_neighbours(self, bomb_indicies):


        def increment_around_bomb(y,x):
            if type(neighbours_map[y][x]) == int:
                neighbours_map[y][x] += 1

        neighbours_map=[]
        for _ in range(self.height):
            neighbours_map.append([0]*self.width)

        for bomb_y,bomb_x in bomb_indicies:
            neighbours_map[bomb_y][bomb_x] = "bomb"

            self.iterate_over_neighbours(bomb_y, bomb_x, increment_around_bomb)

        neighbours_map = [[str(x) for x in row] for row in neighbours_map]

        return neighbours_map


    def button_coordinates(self,button):
        grid_info = button.grid_info()
        button_y, button_x = grid_info['row'],grid_info['column']
        return button_y,button_x


    def field_reveal(self,button):


        def cluster_detection(y,x):
            if str(self.minefield[y][x].cget('image')) == str(self.assets['empty']):                           
                self.field_reveal(self.minefield[y][x])
                if self.neighbours_map[y][x] == 'bomb':
                    self.reveal_all()
                    print('YOU LOST :(')


        def count_adjacent_flags(y,x):
            if str(self.minefield[y][x].cget('image')) == str(self.assets['flag']):
                self.adjacent_flags +=1

        button_y, button_x = self.button_coordinates(button)

        if str(button.cget('image')) == str(self.assets['empty']):
            
            image = self.neighbours_map[button_y][button_x]
            button.configure(image=self.assets[self.neighbours_map[button_y][button_x]])

            if image == '0':
                self.iterate_over_neighbours(button_y, button_x, cluster_detection)
                    
            #print('image assigned')
            self.fields_revealed += 1
            return image
       
        elif str(button.cget('image')) != str(self.assets['flag']):
            image = self.neighbours_map[button_y][button_x]
            self.adjacent_flags = 0
            self.iterate_over_neighbours(button_y,button_x,count_adjacent_flags)
            if str(self.adjacent_flags) == image:
                self.iterate_over_neighbours(button_y, button_x, cluster_detection)
            return image

    def reveal_all(self):
        for row in self.minefield:
            for button in row:
                self.field_reveal(button)
    
    def read_assets(self):
        self.assets={}
        assets_path='assets/'
        assets_contents=[file for file in os.listdir(assets_path)]
        for file_name in assets_contents:
            image_path = os.path.join(assets_path,file_name)
            image = tk.PhotoImage(file=image_path)
            self.assets[file_name.split('.')[0]] = image
        