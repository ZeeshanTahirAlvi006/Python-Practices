import pygame,random,math,sys
from enum import Enum
from collections import deque
import numpy as np

grid_size = 4
cell_size = 110
info_size = 420
width,height = grid_size*cell_size+info_size,grid_size*cell_size+100
FPS=30

COLORS = {
    'bg':(8,6,18),
    "obstacle": (12,8,28),
    "wumpus":(18,12,40),
    "pink":(255,105,180),
    "yellow":(255,255,0),
    "cyan" :(0,255,255),
    "danger":(255,0,0),
    "text":(255,255,255)
}

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class World:
    def __init__(self,seed=None):
        if seed is not None:
            random.seed(seed)
            self.reset()
        def reset(self):
            self.grid = np.zeros((grid_size,grid_size),dtype= int)
            self.player_pos = (0,0)
            self.player_direction = Direction.RIGHT
            self.alive = True
            self.arrow = 1
            self.gold = 0
            self.over = 0
            self.win = False
            self.score = 0
            self.place()

        def place(self):
            def rnd():
                return random.randint(0,grid_size-1),random.randint(0,grid_size-1)
                while True:
                    x,y = rnd()
                    if(x,y) != (0,0):
                        self.grid[x][y]['wumpus'] = 1
                        self.wumpus_pos = (x,y);
                        break
                while True:
                    x,y = rnd()
                    if(x,y)!=(0,0) and not sum(self.grid[x][y].values()):
                        self.grid[x][y]['obstacle']=1
                        c+=1
                self.percepts()
        def percepts(self):
            for y in range(grid_size):
                for x in range(grid_size):
                    self.grid[x][y]['stench']=0
                    self.grid[x][y]['breeze']=0
            if self.alive:
                x,y = self.wumpus_pos
            for dx,dy in[(0,1),(0,-1),(1,0),(-1,0)]:
                nx,ny = x+dx,y+dy
                if 0<=nx<grid_size and 0<=ny<grid_size:
                    self.grid[nx][ny]['stench']=1
            for y in range(grid_size):
                for x in range(grid_size):
                    if self.grid[x][y]['obstacle']:
                        for dx,dy in[(0,1),(0,-1),(1,0),(-1,0)]:
                            nx,ny = x+dx,y+dy
                            if 0<=nx<grid_size and 0<=ny<grid_size:
                                self.grid[nx][ny]['breeze']=1
        def move(self):
            if self.over:
                return
            x,y  = self.player_pos
            dx,dy = [(0,-1),(1,0),(0,1),(-1,0)][self.player_direction.value]
            nx,ny = x+dx,y+dy
            if not (0<=nx<grid_size and 0<=ny<grid_size):
                return
            self.player_pos = (nx,ny)
            self.score -= 1
            cell = self.grid[nx][ny]
            if cell['player'] or (cell['wumpus'] or cell['obstacle'] and self.alive):
                self.score -= 100
                self.over = 1
        def shoot(self):
            if not self.arrow:
                return
            self.arrow = 0
            self.score -= 10
            x,y = self.player_pos
            dx,dy = [(0,-1),(1,0),(0,1),(-1,0)][self.player_direction.value]
            while 0<=x+dx<grid_size and 0<=y+dy<grid_size:
                x,y = x+dx,y+dy
                if not (0<=x<grid_size and 0<=y<grid_size):
                    break
                if self.grid[x][y]['wumpus']:
                    self.alive = False
                    self.percepts()
                    break
class Agent:
    pass
