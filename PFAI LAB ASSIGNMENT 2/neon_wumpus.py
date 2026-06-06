import pygame, random, sys
from enum import Enum
import numpy as np
from collections import deque

grid_size = 4
cell_size = 130
info_w = 300
width = grid_size * cell_size + info_w
height = grid_size * cell_size
FPS = 4

COLORS = {
    'bg':       (8,   6,  18),
    'cell':     (18, 14,  40),
    'visited':  (22, 18,  50),
    'obstacle': (10,  8,  24),
    'wumpus':   (120, 20, 20),
    'dead_w':   (50,  10, 10),
    'player':   (255,220,  0),
    'gold':     (255,180,  0),
    'stench':   (180,  0,180),
    'breeze':   (0,  180,220),
    'safe':     (0,  200, 80),
    'danger':   (200,  0,  0),
    'unknown':  (80,  80, 80),
    'text':     (255,255,255),
    'dim':      (120,120,140),
    'grid':     (30,  25, 60),
    'arrow':    (255,100,  0),
}

DIR_DELTA = [(0,-1),(1,0),(0,1),(-1,0)]

class Dir(Enum):
    UP=0; RIGHT=1; DOWN=2; LEFT=3

class World:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.reset()
    def make_cell(self):
        return {'player':0,'wumpus':0,'obstacle':0,'stench':0,'breeze':0,'gold':0}
    def reset(self):
        self.grid = np.array([[self.make_cell() for _ in range(grid_size)] for _ in range(grid_size)], dtype=object)
        self.player_pos = (0,0)
        self.player_dir = Dir.RIGHT
        self.wumpus_alive = True
        self.arrow = 1
        self.gold_grabbed = False
        self.over = False
        self.win = False
        self.score = 0
        self.last_action = ''
        self.grid[0][0]['player'] = 1
        self.place()
    def place(self):
        def rnd(): return random.randint(0,grid_size-1), random.randint(0,grid_size-1)
        while True:
            x,y = rnd()
            if (x,y)!=(0,0):
                self.grid[x][y]['wumpus']=1; self.wumpus_pos=(x,y); break
        while True:
            x,y = rnd()
            if (x,y)!=(0,0) and not any(self.grid[x][y].values()):
                self.grid[x][y]['obstacle']=1; break
        while True:
            x,y = rnd()
            if (x,y)!=(0,0) and not any(self.grid[x][y].values()):
                self.grid[x][y]['gold']=1; break
        self.update_percepts()
    def update_percepts(self):
        for x in range(grid_size):
            for y in range(grid_size):
                self.grid[x][y]['stench']=0; self.grid[x][y]['breeze']=0
        if self.wumpus_alive:
            wx,wy = self.wumpus_pos
            for dx,dy in DIR_DELTA:
                nx,ny = wx+dx,wy+dy
                if 0<=nx<grid_size and 0<=ny<grid_size:
                    self.grid[nx][ny]['stench']=1
        for x in range(grid_size):
            for y in range(grid_size):
                if self.grid[x][y]['obstacle']:
                    for dx,dy in DIR_DELTA:
                        nx,ny = x+dx,y+dy
                        if 0<=nx<grid_size and 0<=ny<grid_size:
                            self.grid[nx][ny]['breeze']=1
    def neighbors(self, x, y):
        return [(x+dx,y+dy) for dx,dy in DIR_DELTA if 0<=x+dx<grid_size and 0<=y+dy<grid_size]
    def move_forward(self):
        if self.over: return False
        x,y = self.player_pos
        dx,dy = DIR_DELTA[self.player_dir.value]
        nx,ny = x+dx,y+dy
        if not (0<=nx<grid_size and 0<=ny<grid_size):
            self.last_action='bump'; return False
        self.grid[x][y]['player']=0
        self.player_pos=(nx,ny)
        self.grid[nx][ny]['player']=1
        self.score -= 1
        cell = self.grid[nx][ny]
        if cell['obstacle']:
            self.score -= 100; self.over=True; self.last_action='hit wall'; return True
        if cell['wumpus'] and self.wumpus_alive:
            self.score -= 1000; self.over=True; self.last_action='eaten'; return True
        self.last_action='move'
        return True
    def turn_to(self, tx, ty):
        x,y = self.player_pos
        dx,dy = tx-x, ty-y
        if dx==1:  self.player_dir=Dir.RIGHT
        elif dx==-1: self.player_dir=Dir.LEFT
        elif dy==1:  self.player_dir=Dir.DOWN
        elif dy==-1: self.player_dir=Dir.UP
    def shoot(self):
        if not self.arrow or self.over: return
        self.arrow=0; self.score-=10; self.last_action='shoot'
        x,y = self.player_pos
        dx,dy = DIR_DELTA[self.player_dir.value]
        cx,cy = x,y
        while True:
            cx+=dx; cy+=dy
            if not (0<=cx<grid_size and 0<=cy<grid_size): break
            if self.grid[cx][cy]['wumpus']:
                self.grid[cx][cy]['wumpus']=0
                self.wumpus_alive=False
                self.update_percepts()
                self.last_action='killed wumpus!'; break
    def grab_gold(self):
        x,y = self.player_pos
        if self.grid[x][y]['gold']:
            self.grid[x][y]['gold']=0
            self.gold_grabbed=True
            self.score+=1000
            self.last_action='grabbed gold!'
    def cell(self, x, y): return self.grid[x][y]



class KB:
    def __init__(self):
        self.cells = np.array([[self._blank() for _ in range(grid_size)] for _ in range(grid_size)], dtype=object)
        self.cells[0][0]['safe']=True; self.cells[0][0]['wumpus_p']=False; self.cells[0][0]['pit_p']=False
    def _blank(self):
        return {'visited':False,'safe':False,'wumpus_p':True,'pit_p':True,'stench':False,'breeze':False}
    def c(self,x,y): return self.cells[x][y]
    def observe(self, world):
        x,y = world.player_pos
        cell = world.cell(x,y)
        kb = self.c(x,y)
        kb['visited']=True; kb['safe']=True; kb['wumpus_p']=False; kb['pit_p']=False
        kb['stench']=cell['stench']; kb['breeze']=cell['breeze']
        nbrs = world.neighbors(x,y)
        if not cell['stench']:
            for nx,ny in nbrs: self.c(nx,ny)['wumpus_p']=False
        if not cell['breeze']:
            for nx,ny in nbrs: self.c(nx,ny)['pit_p']=False
        # propagate: if a neighbor is wumpus_p=False and pit_p=False → safe
        for nx,ny in nbrs:
            n = self.c(nx,ny)
            if not n['wumpus_p'] and not n['pit_p']: n['safe']=True
        self.infer_wumpus(world)
    def infer_wumpus(self, world):
        # if only one cell across all stench neighbors is still wumpus_possible → it's the wumpus
        candidates = set()
        for x in range(grid_size):
            for y in range(grid_size):
                if self.c(x,y)['visited'] and self.c(x,y)['stench']:
                    nbr_candidates = [(nx,ny) for nx,ny in world.neighbors(x,y) if self.c(nx,ny)['wumpus_p']]
                    if not candidates: candidates = set(nbr_candidates)
                    else: candidates &= set(nbr_candidates)
        if len(candidates)==1:
            wx,wy = next(iter(candidates))
            # mark all others as wumpus_p=False
            for x in range(grid_size):
                for y in range(grid_size):
                    if (x,y)!=(wx,wy): self.c(x,y)['wumpus_p']=False
            # those cells may now be safe
            for x in range(grid_size):
                for y in range(grid_size):
                    n=self.c(x,y)
                    if not n['wumpus_p'] and not n['pit_p']: n['safe']=True
    def safe_unvisited(self, world):
        return [(x,y) for x in range(grid_size) for y in range(grid_size)
                if self.c(x,y)['safe'] and not self.c(x,y)['visited']]
    def wumpus_target(self):
        # return cell if exactly one candidate remains
        cands = [(x,y) for x in range(grid_size) for y in range(grid_size) if self.c(x,y)['wumpus_p']]
        return cands[0] if len(cands)==1 else None


class Agent:
    def __init__(self, world):
        self.world = world
        self.kb = KB()
        self.path = deque()          # planned steps (x,y) to walk
        self.done = False
    def bfs(self, start, goals):
        # returns list of (x,y) steps from start to nearest goal (excluding start)
        if not goals: return []
        visited = {start}; queue = deque([[start]])
        while queue:
            path = queue.popleft()
            x,y = path[-1]
            if (x,y) in goals: return path[1:]
            for nx,ny in self.world.neighbors(x,y):
                if (nx,ny) not in visited and self.kb.c(nx,ny)['safe']:
                    visited.add((nx,ny)); queue.append(path+[(nx,ny)])
        return []
    def face_and_step(self, tx, ty):
        self.world.turn_to(tx,ty)
        self.world.move_forward()
    def try_shoot_wumpus(self):
        if not self.world.arrow or not self.world.wumpus_alive: return False
        target = self.kb.wumpus_target()
        if not target: return False
        tx,ty = target
        x,y = self.world.player_pos
        # only shoot if adjacent and aligned
        if abs(tx-x)+abs(ty-y)==1:
            self.world.turn_to(tx,ty)
            self.world.shoot()
            # after kill, target becomes safe
            if not self.world.wumpus_alive:
                self.kb.c(tx,ty)['wumpus_p']=False; self.kb.c(tx,ty)['safe']=True
            return True
        return False
    def act(self):
        if self.world.over or self.done: return
        w = self.world
        x,y = w.player_pos
        # observe and update KB
        self.kb.observe(w)
        # grab gold if present
        w.grab_gold()
        if w.gold_grabbed and not w.over:
            # navigate back to (0,0)
            if (x,y)==(0,0):
                self.done=True; w.win=True; w.over=True; return
            if not self.path:
                self.path = deque(self.bfs((x,y),{(0,0)}))
            if self.path:
                tx,ty = self.path.popleft()
                self.face_and_step(tx,ty)
            return
        # follow planned path first
        if self.path:
            tx,ty = self.path.popleft()
            self.face_and_step(tx,ty)
            return
        # try to shoot wumpus if localized
        if self.try_shoot_wumpus(): return
        # find safe unvisited cells and plan path
        targets = set(self.kb.safe_unvisited(w))
        if targets:
            path = self.bfs((x,y), targets)
            if path:
                self.path = deque(path)
                tx,ty = self.path.popleft()
                self.face_and_step(tx,ty)
                return
        # no safe moves — give up
        self.done=True; w.over=True


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Wumpus World')
        self.clock = pygame.time.Clock()
        self.font_lg = pygame.font.SysFont('Consolas', 18, bold=True)
        self.font_sm = pygame.font.SysFont('Consolas', 14)
        self.world = World()
        self.agent = Agent(self.world)
        self.auto = True
        self.step_timer = 0
    def cell_rect(self, x, y):
        return pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
    def draw_grid(self):
        kb = self.agent.kb
        for x in range(grid_size):
            for y in range(grid_size):
                cell = self.world.grid[x][y]
                kbc  = kb.c(x,y)
                rect = self.cell_rect(x,y)
                # base color
                if cell['obstacle']:
                    base = COLORS['obstacle']
                elif kbc['visited']:
                    base = COLORS['visited']
                elif kbc['safe']:
                    base = (14,34,24)
                else:
                    base = COLORS['cell']
                pygame.draw.rect(self.screen, base, rect)
                pygame.draw.rect(self.screen, COLORS['grid'], rect, 1)
                cx,cy = rect.centerx, rect.centery
                # wumpus
                if cell['wumpus']:
                    col = COLORS['wumpus'] if self.world.wumpus_alive else COLORS['dead_w']
                    pygame.draw.circle(self.screen, col, (cx,cy), cell_size//3)
                # gold
                if cell['gold']:
                    pygame.draw.polygon(self.screen, COLORS['gold'], self._star(cx,cy,18,9,5))
                # stench ring
                if cell['stench']:
                    pygame.draw.circle(self.screen, COLORS['stench'], (cx,cy), cell_size//3, 2)
                # breeze ring
                if cell['breeze']:
                    pygame.draw.circle(self.screen, COLORS['breeze'], (cx,cy), cell_size//4, 2)
                # KB overlay — tiny dots
                if kbc['wumpus_p'] and not kbc['visited']:
                    pygame.draw.circle(self.screen, COLORS['danger'], (rect.x+10,rect.y+10), 4)
                if kbc['pit_p'] and not kbc['visited']:
                    pygame.draw.circle(self.screen, COLORS['breeze'], (rect.x+10,rect.y+22), 4)
                if kbc['safe'] and not kbc['visited']:
                    pygame.draw.circle(self.screen, COLORS['safe'], (rect.x+10,rect.y+10), 4)
        # player
        px,py = self.world.player_pos
        prect = self.cell_rect(px,py)
        cx,cy = prect.centerx,prect.centery
        # draw direction arrow
        d = self.world.player_dir.value
        adx,ady = DIR_DELTA[d]
        tip = (cx+adx*28, cy+ady*28)
        pygame.draw.circle(self.screen, COLORS['player'], (cx,cy), cell_size//3)
        pygame.draw.line(self.screen, COLORS['arrow'], (cx,cy), tip, 4)
    def _star(self, cx, cy, r_out, r_in, n):
        pts=[]
        for i in range(2*n):
            r = r_out if i%2==0 else r_in
            a = -3.14159/2 + i*3.14159/n
            pts.append((cx+r*__import__('math').cos(a), cy+r*__import__('math').sin(a)))
        return pts
    def draw_info(self):
        ox = grid_size*cell_size+10
        w = self.world
        def txt(s,x,y,col=COLORS['text'],font=None):
            f = font or self.font_lg
            self.screen.blit(f.render(s,True,col),(x,y))
        txt('WUMPUS WORLD', ox, 10)
        txt(f"Score : {w.score}", ox, 38)
        txt(f"Arrow : {'yes' if w.arrow else 'no'}", ox, 58)
        txt(f"Gold  : {'grabbed!' if w.gold_grabbed else 'on map'}", ox, 78)
        txt(f"Wumpus: {'dead' if not w.wumpus_alive else 'alive'}", ox, 98, COLORS['dim'] if not w.wumpus_alive else COLORS['danger'])
        txt(f"Action: {w.last_action}", ox, 120, COLORS['dim'], self.font_sm)
        if w.over:
            msg = 'WIN!' if w.win else 'DEAD'
            col = COLORS['safe'] if w.win else COLORS['danger']
            txt(msg, ox, 150, col)
        txt('─'*18, ox, 170, COLORS['grid'], self.font_sm)
        txt('LEGEND', ox, 185, COLORS['dim'], self.font_sm)
        legend = [
            (COLORS['stench'],  'stench ring'),
            (COLORS['breeze'],  'breeze ring'),
            (COLORS['danger'],  '● wumpus possible'),
            (COLORS['safe'],    '● safe unknown'),
            (COLORS['player'],  '● player'),
            (COLORS['wumpus'],  '● wumpus'),
            (COLORS['gold'],    '★ gold'),
        ]
        for i,(col,label) in enumerate(legend):
            pygame.draw.rect(self.screen, col, (ox,205+i*18,10,10))
            txt(label, ox+14, 204+i*18, COLORS['dim'], self.font_sm)
        txt('SPACE: pause/resume', ox, height-50, COLORS['dim'], self.font_sm)
        txt('R: reset', ox, height-30, COLORS['dim'], self.font_sm)
    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.auto = not self.auto
                    elif event.key==pygame.K_r:
                        self.world=World(); self.agent=Agent(self.world)
                    elif event.key==pygame.K_RIGHT and not self.auto:
                        if not self.world.over: self.agent.act()
            if self.auto and not self.world.over:
                self.agent.act()
            self.screen.fill(COLORS['bg'])
            self.draw_grid()
            self.draw_info()
            pygame.display.flip()

if __name__=='__main__':
    Game().run()