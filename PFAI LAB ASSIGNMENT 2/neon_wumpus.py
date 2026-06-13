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
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.reset()

    def make_cell(self):
        return {
            'player': 0,
            'wumpus': 0,
            'obstacle': 0,
            'stench': 0,
            'breeze': 0,
            'gold': 0
        }

    def reset(self):
        self.grid = np.array([[self.make_cell() for _ in range(grid_size)] for _ in range(grid_size)], dtype=object)
        self.player_pos = (0, 0)
        self.player_direction = Direction.RIGHT
        self.alive = True
        self.arrow = 1
        self.gold = 0
        self.over = 0
        self.win = False
        self.score = 0
        self.grid[0][0]['player'] = 1
        self.place()

    def place(self):
        def rnd():
            return random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)

        while True:
            x, y = rnd()
            if (x, y) != (0, 0):
                self.grid[x][y]['wumpus'] = 1
                self.wumpus_pos = (x, y)
                break

        while True:
            x, y = rnd()
            if (x, y) != (0, 0) and not any(self.grid[x][y].values()):
                self.grid[x][y]['obstacle'] = 1
                break

        while True:
            x, y = rnd()
            if (x, y) != (0, 0) and not any(self.grid[x][y].values()):
                self.grid[x][y]['gold'] = 1
                break

        self.percepts()

    def percepts(self):
        for y in range(grid_size):
            for x in range(grid_size):
                self.grid[x][y]['stench'] = 0
                self.grid[x][y]['breeze'] = 0

        if self.alive:
            x, y = self.wumpus_pos
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    self.grid[nx][ny]['stench'] = 1

        for y in range(grid_size):
            for x in range(grid_size):
                if self.grid[x][y]['obstacle']:
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid_size and 0 <= ny < grid_size:
                            self.grid[nx][ny]['breeze'] = 1

    def move(self):
        if self.over:
            return

        x, y = self.player_pos
        self.grid[x][y]['player'] = 0
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.player_direction.value]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < grid_size and 0 <= ny < grid_size):
            self.grid[x][y]['player'] = 1
            return

        cell = self.grid[nx][ny]
        self.player_pos = (nx, ny)
        self.grid[nx][ny]['player'] = 1
        self.score -= 1
        if cell['wumpus'] or (cell['obstacle'] and self.alive):
            self.score -= 100
            self.over = 1

    def shoot(self):
        if not self.arrow or self.over:
            return

        self.arrow = 0
        self.score -= 10
        x, y = self.player_pos
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.player_direction.value]
        while 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
            x, y = x + dx, y + dy
            if self.grid[x][y]['wumpus']:
                self.alive = False
                self.percepts()
                break

class Agent:
    def __init__(self, world):
        self.world = world
        self.knowledge = np.array([[{'visited': 0, 'stench': 0} for _ in range(grid_size)] for _ in range(grid_size)], dtype=object)

    def act(self):
        x, y = self.world.player_pos
        self.knowledge[x][y]['visited'] = 1
        self.knowledge[x][y]['stench'] = self.world.grid[x][y]['stench']
        if self.world.grid[x][y]['gold']:
            self.world.score += 1000
            self.world.gold = 1
            self.world.grid[x][y]['gold'] = 0

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and self.knowledge[nx][ny]['stench']:
                self.turn(nx, ny)
                return

        self.world.move()
    def turn(self,nx,ny):
        x,y = self.world.player_pos
        if nx>x:
            self.world.player_direction = Direction.RIGHT
        elif nx<x:
            self.world.player_direction = Direction.LEFT~
        elif ny>y:
            self.world.player_direction = Direction.DOWN
        elif ny<y:
            self.world.player_direction = Direction.UP
        self.world.move()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.time.Clock().tick(FPS)
        self.font = pygame.font.SysFont(None, 24)
        self.world = World()
        self.agent = Agent(self.world)
        self.auto = True
    def draw_grid(self):
        for x in range(grid_size):
            for y in range(grid_size):
                cell = self.world.grid[x][y]
                rect = pygame.Rect(x*cell_size,y*cell_size,cell_size,cell_size)
                pygame.draw.rect(self.screen,COLORS['obstacle'] if cell['obstacle'] else COLORS['bg'],rect)
                if cell['wumpus']:
                    pygame.draw.circle(self.screen,COLORS['wumpus'],rect.center,cell_size//3)
                if cell['stench']:
                    pygame.draw.circle(self.screen,COLORS['pink'],rect.center,cell_size//4)
                if cell['breeze']:
                    pygame.draw.circle(self.screen,COLORS['cyan'],rect.center,cell_size//4)
        px,py = self.world.player_pos
        player_rect = pygame.Rect(px*cell_size,py*cell_size,cell_size,cell_size)
        pygame.draw.circle(self.screen,COLORS['yellow'],player_rect.center,cell_size//3)
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.auto = not self.auto
            if self.auto and not self.world.over:
                self.agent.act()
            self.screen.fill(COLORS['bg'])
            self.draw_grid()
            score_text = self.font.render(f'Score: {self.world.score}', True, COLORS['text'])
            self.screen.blit(score_text, (grid_size*cell_size + 20, 20))
            pygame.display.flip()
if __name__ == "__main__":
    Game().run()