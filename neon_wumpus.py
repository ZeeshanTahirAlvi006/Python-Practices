import pygame, random, sys, math
from enum import Enum
from collections import deque

# ─── CONFIG ──────────────────────────────────────────────────────────────────
grid_size = 4
cell_size = 140
info_w = 320
width = grid_size * cell_size + info_w
height = grid_size * cell_size
FPS = 60
AGENT_STEP_INTERVAL = 800  # ms between AI steps

# ─── PREMIUM COLOR PALETTE ──────────────────────────────────────────────────
C = {
    'bg':           (10,   8,  22),
    'cell_dark':    (16,  12,  36),
    'cell_visited': (24,  20,  52),
    'cell_safe':    (16,  38,  28),
    'cell_pit':     (8,    4,  16),
    'grid_line':    (40,  32,  72),
    'fog':          (6,    4,  14),

    'player':       (255, 220,  40),
    'player_glow':  (255, 200,   0),
    'arrow_tip':    (255, 120,  20),

    'wumpus':       (200,  30,  30),
    'wumpus_glow':  (255,  40,  40),
    'wumpus_dead':  (60,   20,  20),

    'pit_ring':     (100,  60, 160),
    'pit_center':   (20,    8,  40),

    'gold':         (255, 200,  50),
    'gold_glow':    (255, 180,   0),

    'stench':       (200,  40, 200),
    'stench_glow':  (255,  80, 255),
    'breeze':       (40,  200, 240),
    'breeze_glow':  (80,  220, 255),

    'safe_dot':     (40,  220, 100),
    'danger_dot':   (220,  40,  40),

    'text':         (240, 235, 255),
    'text_dim':     (120, 115, 145),
    'text_accent':  (180, 140, 255),

    'panel_bg':     (14,  10,  30),
    'panel_border': (50,  40,  90),
    'card_bg':      (22,  18,  44),
    'card_border':  (60,  50, 100),

    'win':          (40,  220, 120),
    'lose':         (220,  50,  50),
    'menu_accent':  (140, 100, 255),
}

DIR_DELTA = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class Dir(Enum):
    UP = 0; RIGHT = 1; DOWN = 2; LEFT = 3


# ═══════════════════════════════════════════════════════════════════════════════
#  PARTICLE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
class Particle:
    def __init__(self, x, y, color, life=1.0, speed=None, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        angle = random.uniform(0, math.tau)
        spd = speed or random.uniform(15, 50)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        alpha = max(0, self.life / self.max_life)
        r = max(1, int(self.size * alpha))
        col = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), r)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, life=1.0, speed=None, size=3):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, life, speed, size))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ═══════════════════════════════════════════════════════════════════════════════
#  WORLD — GAME LOGIC (unchanged from fixed version)
# ═══════════════════════════════════════════════════════════════════════════════
class World:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.reset()

    def make_cell(self):
        return {'player': 0, 'wumpus': 0, 'pit': 0, 'stench': 0,
                'breeze': 0, 'gold': 0, 'glitter': 0}

    def reset(self):
        self.grid = [[self.make_cell() for _ in range(grid_size)]
                      for _ in range(grid_size)]
        self.player_pos = (0, 0)
        self.player_dir = Dir.RIGHT
        self.wumpus_alive = True
        self.arrow = 1
        self.gold_grabbed = False
        self.over = False
        self.win = False
        self.score = 0
        self.moves = 0
        self.last_action = ''
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
        for _ in range(2):  # place 2 pits
            while True:
                x, y = rnd()
                if (x, y) != (0, 0) and not any(self.grid[x][y].values()):
                    self.grid[x][y]['pit'] = 1
                    break
        while True:
            x, y = rnd()
            if (x, y) != (0, 0) and not any(self.grid[x][y].values()):
                self.grid[x][y]['gold'] = 1
                break
        self.update_percepts()
        self.update_glitter()

    def update_glitter(self):
        for x in range(grid_size):
            for y in range(grid_size):
                self.grid[x][y]['glitter'] = 1 if self.grid[x][y]['gold'] else 0

    def update_percepts(self):
        for x in range(grid_size):
            for y in range(grid_size):
                self.grid[x][y]['stench'] = 0
                self.grid[x][y]['breeze'] = 0
        if self.wumpus_alive:
            wx, wy = self.wumpus_pos
            for dx, dy in DIR_DELTA:
                nx, ny = wx + dx, wy + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    self.grid[nx][ny]['stench'] = 1
        for x in range(grid_size):
            for y in range(grid_size):
                if self.grid[x][y]['pit']:
                    for dx, dy in DIR_DELTA:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid_size and 0 <= ny < grid_size:
                            self.grid[nx][ny]['breeze'] = 1

    def neighbors(self, x, y):
        return [(x + dx, y + dy) for dx, dy in DIR_DELTA
                if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size]

    def move_forward(self):
        if self.over:
            return False
        x, y = self.player_pos
        dx, dy = DIR_DELTA[self.player_dir.value]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < grid_size and 0 <= ny < grid_size):
            self.last_action = 'bump'
            return False
        self.grid[x][y]['player'] = 0
        self.player_pos = (nx, ny)
        self.grid[nx][ny]['player'] = 1
        self.score -= 1
        self.moves += 1
        cell = self.grid[nx][ny]
        if cell['pit']:
            self.score -= 1000
            self.over = True
            self.last_action = 'fell into pit'
            return True
        if cell['wumpus'] and self.wumpus_alive:
            self.score -= 1000
            self.over = True
            self.last_action = 'eaten'
            return True
        self.last_action = 'move'
        return True

    def turn_to(self, tx, ty):
        x, y = self.player_pos
        dx, dy = tx - x, ty - y
        if dx == 1:    self.player_dir = Dir.RIGHT
        elif dx == -1: self.player_dir = Dir.LEFT
        elif dy == 1:  self.player_dir = Dir.DOWN
        elif dy == -1: self.player_dir = Dir.UP

    def shoot(self):
        if not self.arrow or self.over:
            return
        self.arrow = 0
        self.score -= 10
        self.last_action = 'shoot'
        x, y = self.player_pos
        dx, dy = DIR_DELTA[self.player_dir.value]
        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < grid_size and 0 <= cy < grid_size):
                break
            if self.grid[cx][cy]['wumpus']:
                self.grid[cx][cy]['wumpus'] = 0
                self.wumpus_alive = False
                self.update_percepts()
                self.last_action = 'killed wumpus!'
                break

    def grab_gold(self):
        x, y = self.player_pos
        if self.grid[x][y]['glitter']:
            self.grid[x][y]['gold'] = 0
            self.grid[x][y]['glitter'] = 0
            self.gold_grabbed = True
            self.score += 1000
            self.last_action = 'grabbed gold!'

    def cell(self, x, y):
        return self.grid[x][y]


# ═══════════════════════════════════════════════════════════════════════════════
#  KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════════════════════
class KB:
    def __init__(self):
        self.cells = [[self._blank() for _ in range(grid_size)]
                       for _ in range(grid_size)]
        self.cells[0][0]['safe'] = True
        self.cells[0][0]['wumpus_p'] = False
        self.cells[0][0]['pit_p'] = False

    def _blank(self):
        return {'visited': False, 'safe': False, 'wumpus_p': True,
                'pit_p': True, 'stench': False, 'breeze': False}

    def c(self, x, y):
        return self.cells[x][y]

    def observe(self, world):
        x, y = world.player_pos
        cell = world.cell(x, y)
        kb = self.c(x, y)
        kb['visited'] = True
        kb['safe'] = True
        kb['wumpus_p'] = False
        kb['pit_p'] = False
        kb['stench'] = cell['stench']
        kb['breeze'] = cell['breeze']
        nbrs = world.neighbors(x, y)
        if not cell['stench']:
            for nx, ny in nbrs:
                self.c(nx, ny)['wumpus_p'] = False
        if not cell['breeze']:
            for nx, ny in nbrs:
                self.c(nx, ny)['pit_p'] = False
        for nx, ny in nbrs:
            n = self.c(nx, ny)
            if not n['wumpus_p'] and not n['pit_p']:
                n['safe'] = True
        self.infer_wumpus(world)

    def infer_wumpus(self, world):
        candidates = set()
        for x in range(grid_size):
            for y in range(grid_size):
                if self.c(x, y)['visited'] and self.c(x, y)['stench']:
                    nbr_cands = [(nx, ny) for nx, ny in world.neighbors(x, y)
                                 if self.c(nx, ny)['wumpus_p']]
                    if not candidates:
                        candidates = set(nbr_cands)
                    else:
                        candidates &= set(nbr_cands)
        if len(candidates) == 1:
            wx, wy = next(iter(candidates))
            for x in range(grid_size):
                for y in range(grid_size):
                    if (x, y) != (wx, wy):
                        self.c(x, y)['wumpus_p'] = False
            for x in range(grid_size):
                for y in range(grid_size):
                    n = self.c(x, y)
                    if not n['wumpus_p'] and not n['pit_p']:
                        n['safe'] = True

    def safe_unvisited(self, world):
        return [(x, y) for x in range(grid_size) for y in range(grid_size)
                if self.c(x, y)['safe'] and not self.c(x, y)['visited']]

    def wumpus_target(self):
        cands = [(x, y) for x in range(grid_size) for y in range(grid_size)
                 if self.c(x, y)['wumpus_p']]
        return cands[0] if len(cands) == 1 else None


# ═══════════════════════════════════════════════════════════════════════════════
#  AGENT
# ═══════════════════════════════════════════════════════════════════════════════
class Agent:
    def __init__(self, world):
        self.world = world
        self.kb = KB()
        self.path = deque()
        self.done = False

    def bfs(self, start, goals):
        if not goals:
            return []
        visited = {start}
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if (x, y) in goals:
                return path[1:]
            for nx, ny in self.world.neighbors(x, y):
                if (nx, ny) not in visited and self.kb.c(nx, ny)['safe']:
                    visited.add((nx, ny))
                    queue.append(path + [(nx, ny)])
        return []

    def face_and_step(self, tx, ty):
        self.world.turn_to(tx, ty)
        self.world.move_forward()

    def try_shoot_wumpus(self):
        if not self.world.arrow or not self.world.wumpus_alive:
            return False
        target = self.kb.wumpus_target()
        if not target:
            return False
        tx, ty = target
        x, y = self.world.player_pos
        if abs(tx - x) + abs(ty - y) == 1:
            self.world.turn_to(tx, ty)
            self.world.shoot()
            if not self.world.wumpus_alive:
                self.kb.c(tx, ty)['wumpus_p'] = False
                self.kb.c(tx, ty)['safe'] = True
            return True
        return False

    def act(self):
        if self.world.over or self.done:
            return
        w = self.world
        x, y = w.player_pos
        self.kb.observe(w)
        w.grab_gold()
        if w.gold_grabbed and not w.over:
            if (x, y) == (0, 0):
                self.done = True
                w.win = True
                w.over = True
                return
            if not self.path:
                self.path = deque(self.bfs((x, y), {(0, 0)}))
            if self.path:
                tx, ty = self.path.popleft()
                self.face_and_step(tx, ty)
            return
        if self.path:
            tx, ty = self.path.popleft()
            self.face_and_step(tx, ty)
            return
        if self.try_shoot_wumpus():
            return
        targets = set(self.kb.safe_unvisited(w))
        if targets:
            path = self.bfs((x, y), targets)
            if path:
                self.path = deque(path)
                tx, ty = self.path.popleft()
                self.face_and_step(tx, ty)
                return
        self.done = True
        w.over = True


# ═══════════════════════════════════════════════════════════════════════════════
#  DRAWING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB colors."""
    t = max(0, min(1, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_glow_circle(surf, color, center, radius, intensity=0.3):
    """Draw a soft glow around a circle."""
    for i in range(3, 0, -1):
        r = radius + i * 6
        alpha = intensity / i
        glow_col = tuple(min(255, int(c * alpha)) for c in color)
        pygame.draw.circle(surf, glow_col, center, r)


def draw_rounded_rect(surf, color, rect, radius=8, border=0, border_color=None):
    """Draw a rounded rectangle."""
    r = pygame.Rect(rect)
    pygame.draw.rect(surf, color, r, border_radius=radius)
    if border > 0 and border_color:
        pygame.draw.rect(surf, border_color, r, border, border_radius=radius)


def ease_in_out(t):
    """Smooth ease in-out function."""
    return t * t * (3 - 2 * t)


# ═══════════════════════════════════════════════════════════════════════════════
#  GAME — MAIN CLASS WITH PREMIUM UI
# ═══════════════════════════════════════════════════════════════════════════════
class Game:
    # ── game states ──
    STATE_MENU = 0
    STATE_PLAY = 1
    STATE_OVER = 2

    # ── play modes ──
    MODE_AI = 'ai'
    MODE_MANUAL = 'manual'

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('⚔ Wumpus World — AI Explorer')
        self.clock = pygame.time.Clock()

        # fonts
        self.font_title = pygame.font.SysFont('Segoe UI', 52, bold=True)
        self.font_subtitle = pygame.font.SysFont('Segoe UI', 22)
        self.font_lg = pygame.font.SysFont('Consolas', 17, bold=True)
        self.font_md = pygame.font.SysFont('Consolas', 15)
        self.font_sm = pygame.font.SysFont('Consolas', 13)
        self.font_icon = pygame.font.SysFont('Segoe UI Emoji', 28)
        self.font_big_icon = pygame.font.SysFont('Segoe UI Emoji', 42)

        # particle system
        self.particles = ParticleSystem()

        # timing
        self.time = 0
        self.step_timer = 0
        self.state = self.STATE_MENU
        self.menu_time = 0

        # init game objects
        self.world = World()
        self.agent = Agent(self.world)
        self.play_mode = self.MODE_AI
        self.auto = True
        self.prev_action = ''
        self.menu_selection = 0  # 0 = AI, 1 = Manual

        # screen shake
        self.shake_amount = 0
        self.shake_decay = 8

        # action log
        self.action_log = []

    def new_game(self, mode=None):
        self.world = World()
        self.agent = Agent(self.world)
        if mode:
            self.play_mode = mode
        self.auto = (self.play_mode == self.MODE_AI)
        self.step_timer = 0
        self.prev_action = ''
        self.shake_amount = 0
        self.action_log = []
        self.state = self.STATE_PLAY

    # ── cell coordinates ──
    def cell_rect(self, x, y):
        return pygame.Rect(x * cell_size + 2, y * cell_size + 2,
                           cell_size - 4, cell_size - 4)

    def cell_center(self, x, y):
        return (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)

    # ══════════════════════════════════════════════════════════════════════════
    #  DRAW: GRID
    # ══════════════════════════════════════════════════════════════════════════
    def draw_grid(self):
        kb = self.agent.kb
        t = self.time

        # outer grid border
        grid_w = grid_size * cell_size
        grid_h = grid_size * cell_size
        pygame.draw.rect(self.screen, C['grid_line'],
                         (0, 0, grid_w, grid_h), 2, border_radius=4)

        for x in range(grid_size):
            for y in range(grid_size):
                cell = self.world.grid[x][y]
                kbc = kb.c(x, y)
                rect = self.cell_rect(x, y)
                cx, cy = self.cell_center(x, y)

                # ── base cell color ──
                if kbc['visited']:
                    base = C['cell_visited']
                elif kbc['safe']:
                    base = C['cell_safe']
                else:
                    base = C['cell_dark']

                # fog of war: unvisited cells are darker
                if not kbc['visited'] and not kbc['safe']:
                    base = C['fog']

                draw_rounded_rect(self.screen, base, rect, radius=6,
                                  border=1, border_color=C['grid_line'])

                # ── PIT ──
                if cell['pit'] and kbc['visited']:
                    # dark swirling pit
                    pygame.draw.circle(self.screen, C['pit_center'], (cx, cy), 30)
                    for i in range(3):
                        r = 34 + i * 5
                        pulse = math.sin(t * 2 + i * 1.2) * 0.3 + 0.7
                        col = tuple(int(c * pulse) for c in C['pit_ring'])
                        pygame.draw.circle(self.screen, col, (cx, cy), r, 2)
                    # label
                    lbl = self.font_sm.render('PIT', True, C['pit_ring'])
                    self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 32))

                # ── WUMPUS ──
                if cell['wumpus']:
                    if self.world.wumpus_alive:
                        # pulsing glow
                        pulse = math.sin(t * 3) * 0.2 + 0.8
                        glow_col = tuple(int(c * pulse) for c in C['wumpus_glow'])
                        draw_glow_circle(self.screen, glow_col, (cx, cy), 28, 0.25)
                        pygame.draw.circle(self.screen, C['wumpus'], (cx, cy), 28)
                        # eyes
                        pygame.draw.circle(self.screen, (255, 255, 80), (cx - 9, cy - 6), 5)
                        pygame.draw.circle(self.screen, (255, 255, 80), (cx + 9, cy - 6), 5)
                        pygame.draw.circle(self.screen, (0, 0, 0), (cx - 9, cy - 6), 2)
                        pygame.draw.circle(self.screen, (0, 0, 0), (cx + 9, cy - 6), 2)
                        # mouth
                        pygame.draw.arc(self.screen, (180, 0, 0),
                                        (cx - 12, cy + 2, 24, 14), 3.14, 6.28, 2)
                        lbl = self.font_sm.render('WUMPUS', True, C['wumpus'])
                        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 32))
                    else:
                        pygame.draw.circle(self.screen, C['wumpus_dead'], (cx, cy), 22)
                        # X eyes
                        for ox in [-9, 9]:
                            pygame.draw.line(self.screen, (80, 30, 30),
                                             (cx + ox - 4, cy - 10), (cx + ox + 4, cy - 2), 2)
                            pygame.draw.line(self.screen, (80, 30, 30),
                                             (cx + ox + 4, cy - 10), (cx + ox - 4, cy - 2), 2)

                # ── GOLD ──
                if cell['gold']:
                    # sparkle particles periodically
                    if random.random() < 0.08:
                        self.particles.emit(
                            cx + random.randint(-20, 20),
                            cy + random.randint(-20, 20),
                            C['gold'], count=2, life=0.6, speed=20, size=2
                        )
                    # glow
                    pulse = math.sin(t * 4) * 0.3 + 0.7
                    glow_col = tuple(int(c * pulse) for c in C['gold_glow'])
                    draw_glow_circle(self.screen, glow_col, (cx, cy), 18, 0.3)
                    # star shape
                    self._draw_star(cx, cy, 20, 10, 5, C['gold'])
                    lbl = self.font_sm.render('GOLD', True, C['gold'])
                    self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 28))

                # ── PERCEPTS ──
                # stench ring (pulsing purple)
                if cell['stench'] and kbc['visited']:
                    pulse = math.sin(t * 2.5) * 0.3 + 0.7
                    col = tuple(int(c * pulse) for c in C['stench'])
                    for i in range(2):
                        r = cell_size // 3 - i * 4
                        pygame.draw.circle(self.screen, col, (cx, cy), r, 2)
                    # small label
                    lbl = self.font_sm.render('stench', True, C['stench'])
                    self.screen.blit(lbl, (rect.x + 4, rect.bottom - 16))

                # breeze ring (pulsing cyan)
                if cell['breeze'] and kbc['visited']:
                    pulse = math.sin(t * 3 + 1) * 0.3 + 0.7
                    col = tuple(int(c * pulse) for c in C['breeze'])
                    for i in range(2):
                        r = cell_size // 4 - i * 3
                        pygame.draw.circle(self.screen, col, (cx, cy), r, 2)
                    lbl = self.font_sm.render('breeze', True, C['breeze'])
                    self.screen.blit(lbl, (rect.right - 48, rect.bottom - 16))

                # ── KB OVERLAY DOTS ──
                dot_y = rect.y + 8
                if kbc['wumpus_p'] and not kbc['visited']:
                    pygame.draw.circle(self.screen, C['danger_dot'],
                                       (rect.x + 12, dot_y), 4)
                    pygame.draw.circle(self.screen, C['danger_dot'],
                                       (rect.x + 12, dot_y), 7, 1)
                if kbc['pit_p'] and not kbc['visited']:
                    pygame.draw.circle(self.screen, C['breeze'],
                                       (rect.x + 24, dot_y), 4)
                if kbc['safe'] and not kbc['visited']:
                    pulse = math.sin(t * 2 + x + y) * 0.3 + 0.7
                    col = tuple(int(c * pulse) for c in C['safe_dot'])
                    pygame.draw.circle(self.screen, col, (rect.x + 12, dot_y), 5)
                    # small checkmark
                    lbl = self.font_sm.render('safe', True, col)
                    self.screen.blit(lbl, (rect.x + 20, dot_y - 6))

        # ── PLAYER ──
        px, py = self.world.player_pos
        pcx, pcy = self.cell_center(px, py)

        # glow
        pulse = math.sin(t * 5) * 0.15 + 0.85
        glow_col = tuple(int(c * pulse) for c in C['player_glow'])
        draw_glow_circle(self.screen, glow_col, (pcx, pcy), 26, 0.35)

        # body
        pygame.draw.circle(self.screen, C['player'], (pcx, pcy), 26)
        pygame.draw.circle(self.screen, (200, 170, 0), (pcx, pcy), 26, 2)

        # direction arrow
        d = self.world.player_dir.value
        adx, ady = DIR_DELTA[d]
        tip = (pcx + adx * 32, pcy + ady * 32)
        pygame.draw.line(self.screen, C['arrow_tip'], (pcx, pcy), tip, 4)
        # arrowhead
        perp_x, perp_y = -ady, adx
        head_back = (tip[0] - adx * 10, tip[1] - ady * 10)
        p1 = (head_back[0] + perp_x * 6, head_back[1] + perp_y * 6)
        p2 = (head_back[0] - perp_x * 6, head_back[1] - perp_y * 6)
        pygame.draw.polygon(self.screen, C['arrow_tip'], [tip, p1, p2])

        # agent face
        eye_offset_x = adx * 5
        eye_offset_y = ady * 5
        pygame.draw.circle(self.screen, (40, 30, 0),
                           (pcx - 7 + eye_offset_x, pcy - 4 + eye_offset_y), 3)
        pygame.draw.circle(self.screen, (40, 30, 0),
                           (pcx + 7 + eye_offset_x, pcy - 4 + eye_offset_y), 3)

        # cell coordinate labels (subtle)
        for x in range(grid_size):
            for y in range(grid_size):
                lbl = self.font_sm.render(f'{x},{y}', True, (30, 25, 55))
                r = self.cell_rect(x, y)
                self.screen.blit(lbl, (r.right - 22, r.y + 4))

    def _draw_star(self, cx, cy, r_out, r_in, n, color):
        pts = []
        for i in range(2 * n):
            r = r_out if i % 2 == 0 else r_in
            a = -math.pi / 2 + i * math.pi / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pygame.draw.polygon(self.screen, color, pts)
        # inner highlight
        inner_pts = []
        for i in range(2 * n):
            r = (r_out * 0.6) if i % 2 == 0 else (r_in * 0.6)
            a = -math.pi / 2 + i * math.pi / n
            inner_pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pygame.draw.polygon(self.screen, (255, 240, 150), inner_pts)

    # ══════════════════════════════════════════════════════════════════════════
    #  DRAW: INFO PANEL (SIDEBAR)
    # ══════════════════════════════════════════════════════════════════════════
    def draw_info_panel(self):
        w = self.world
        ox = grid_size * cell_size
        panel_rect = (ox, 0, info_w, height)

        # panel background
        pygame.draw.rect(self.screen, C['panel_bg'], panel_rect)
        pygame.draw.line(self.screen, C['panel_border'],
                         (ox, 0), (ox, height), 2)

        y_cursor = 16
        pad = ox + 16

        # ── TITLE ──
        title = self.font_lg.render('WUMPUS WORLD', True, C['text_accent'])
        self.screen.blit(title, (pad, y_cursor))
        y_cursor += 28

        mode_name = 'AI Agent Explorer' if self.play_mode == self.MODE_AI else 'Manual Play'
        subtitle = self.font_sm.render(mode_name, True, C['text_dim'])
        self.screen.blit(subtitle, (pad, y_cursor))
        y_cursor += 30

        # separator
        pygame.draw.line(self.screen, C['card_border'],
                         (pad, y_cursor), (ox + info_w - 16, y_cursor), 1)
        y_cursor += 14

        # ── STATUS CARDS ──
        card_w = info_w - 32

        def draw_card(label, value, color, yy):
            card_r = pygame.Rect(pad, yy, card_w, 38)
            draw_rounded_rect(self.screen, C['card_bg'], card_r, radius=6,
                              border=1, border_color=C['card_border'])
            lbl = self.font_md.render(label, True, C['text_dim'])
            val = self.font_md.render(str(value), True, color)
            self.screen.blit(lbl, (pad + 10, yy + 10))
            self.screen.blit(val, (pad + card_w - val.get_width() - 10, yy + 10))
            return yy + 46

        y_cursor = draw_card('Score', w.score,
                             C['win'] if w.score >= 0 else C['lose'], y_cursor)
        y_cursor = draw_card('Moves', w.moves, C['text'], y_cursor)
        y_cursor = draw_card('Arrow', 'Ready' if w.arrow else 'Used',
                             C['gold'] if w.arrow else C['text_dim'], y_cursor)
        y_cursor = draw_card('Gold',
                             'Grabbed!' if w.gold_grabbed else 'On Map',
                             C['gold'] if w.gold_grabbed else C['text_dim'],
                             y_cursor)
        y_cursor = draw_card('Wumpus',
                             'Alive' if w.wumpus_alive else 'Dead',
                             C['lose'] if w.wumpus_alive else C['safe_dot'],
                             y_cursor)
        y_cursor += 4

        # ── LAST ACTION ──
        if w.last_action:
            action_color = C['text']
            if 'gold' in w.last_action:
                action_color = C['gold']
            elif 'killed' in w.last_action:
                action_color = C['win']
            elif 'pit' in w.last_action or 'eaten' in w.last_action:
                action_color = C['lose']

            action_card = pygame.Rect(pad, y_cursor, card_w, 32)
            draw_rounded_rect(self.screen, (30, 20, 55), action_card,
                              radius=6, border=1, border_color=C['card_border'])
            act_lbl = self.font_sm.render(f'> {w.last_action}', True, action_color)
            self.screen.blit(act_lbl, (pad + 10, y_cursor + 8))
            y_cursor += 40

        # ── ACTION LOG ──
        y_cursor += 4
        pygame.draw.line(self.screen, C['card_border'],
                         (pad, y_cursor), (ox + info_w - 16, y_cursor), 1)
        y_cursor += 8
        log_title = self.font_sm.render('ACTION LOG', True, C['text_dim'])
        self.screen.blit(log_title, (pad, y_cursor))
        y_cursor += 18

        # show last N actions
        visible_log = self.action_log[-6:]
        for i, entry in enumerate(visible_log):
            alpha = 0.4 + 0.1 * i
            col = tuple(int(c * min(1, alpha)) for c in C['text_dim'])
            line = self.font_sm.render(entry, True, col)
            self.screen.blit(line, (pad + 4, y_cursor))
            y_cursor += 15

        # ── LEGEND ──
        legend_y = height - 180
        pygame.draw.line(self.screen, C['card_border'],
                         (pad, legend_y), (ox + info_w - 16, legend_y), 1)
        legend_y += 8
        ltitle = self.font_sm.render('LEGEND', True, C['text_dim'])
        self.screen.blit(ltitle, (pad, legend_y))
        legend_y += 20

        legend_items = [
            (C['player'],     '● Agent'),
            (C['wumpus'],     '● Wumpus'),
            (C['gold'],       '★ Gold'),
            (C['stench'],     '○ Stench zone'),
            (C['breeze'],     '○ Breeze zone'),
            (C['danger_dot'], '● Wumpus possible'),
            (C['safe_dot'],   '● Safe (inferred)'),
        ]
        for col, label in legend_items:
            pygame.draw.circle(self.screen, col, (pad + 6, legend_y + 5), 4)
            txt = self.font_sm.render(label, True, C['text_dim'])
            self.screen.blit(txt, (pad + 18, legend_y - 1))
            legend_y += 17

        # ── CONTROLS ──
        ctrl_y = height - 50
        if self.play_mode == self.MODE_AI:
            ctrls1 = 'SPACE: pause  |  R: restart'
            ctrls2 = '→: step  |  ESC: menu'
        else:
            ctrls1 = 'WASD/Arrows: move  |  F: shoot'
            ctrls2 = 'G: grab gold  |  C: climb out'
        ctrl_text1 = self.font_sm.render(ctrls1, True, (60, 55, 85))
        ctrl_text2 = self.font_sm.render(ctrls2, True, (60, 55, 85))
        self.screen.blit(ctrl_text1, (pad, ctrl_y))
        self.screen.blit(ctrl_text2, (pad, ctrl_y + 15))

    # ══════════════════════════════════════════════════════════════════════════
    #  DRAW: MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def draw_menu(self):
        self.screen.fill(C['bg'])
        t = self.menu_time

        # animated background grid
        for x in range(grid_size + 4):
            for y in range(grid_size + 3):
                bx = x * 90 + 40
                by = y * 90 + 80
                pulse = math.sin(t * 1.5 + x * 0.7 + y * 0.5) * 0.3 + 0.3
                col = tuple(int(c * pulse) for c in C['grid_line'])
                r = pygame.Rect(bx, by, 80, 80)
                pygame.draw.rect(self.screen, col, r, 1, border_radius=6)

        # title with glow
        mid_x = width // 2
        mid_y = height // 2 - 120

        # glow behind title
        glow_pulse = math.sin(t * 2) * 0.2 + 0.8
        glow_r = int(120 * glow_pulse)
        glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*C['menu_accent'], 20),
                           (glow_r, glow_r), glow_r)
        self.screen.blit(glow_surf,
                         (mid_x - glow_r, mid_y - glow_r + 10))

        title = self.font_title.render('WUMPUS WORLD', True, C['text'])
        tr = title.get_rect(center=(mid_x, mid_y))
        self.screen.blit(title, tr)

        sub = self.font_subtitle.render('Intelligent AI Explorer', True, C['text_accent'])
        sr = sub.get_rect(center=(mid_x, mid_y + 45))
        self.screen.blit(sub, sr)

        # description
        desc_lines = [
            'Navigate a dangerous 4\u00d74 grid world',
            'Find the gold \u2022 Avoid the Wumpus & pits \u2022 Return home',
        ]
        for i, line in enumerate(desc_lines):
            dl = self.font_md.render(line, True, C['text_dim'])
            dr = dl.get_rect(center=(mid_x, mid_y + 90 + i * 22))
            self.screen.blit(dl, dr)

        # ── MODE SELECTION LABEL ──
        mode_label_y = mid_y + 148
        ml = self.font_lg.render('SELECT PLAY MODE', True, C['text_accent'])
        mlr = ml.get_rect(center=(mid_x, mode_label_y))
        self.screen.blit(ml, mlr)

        # ── MODE BUTTONS ──
        btn_w, btn_h = 260, 56
        gap = 16
        btn_ai_y = mode_label_y + 30
        btn_manual_y = btn_ai_y + btn_h + gap

        btn_ai_rect = pygame.Rect(mid_x - btn_w // 2, btn_ai_y, btn_w, btn_h)
        btn_manual_rect = pygame.Rect(mid_x - btn_w // 2, btn_manual_y, btn_w, btn_h)

        # Determine hover state from mouse
        mx, my = pygame.mouse.get_pos()
        if btn_ai_rect.collidepoint(mx, my):
            self.menu_selection = 0
        elif btn_manual_rect.collidepoint(mx, my):
            self.menu_selection = 1

        for i, (rect, label, desc) in enumerate([
            (btn_ai_rect, 'AI AUTO-PLAY', 'Watch the AI agent solve it'),
            (btn_manual_rect, 'MANUAL PLAY', 'Use keyboard to play yourself'),
        ]):
            selected = (self.menu_selection == i)
            if selected:
                pulse = math.sin(t * 3) * 0.12 + 0.88
                btn_col = tuple(int(c * pulse) for c in C['menu_accent'])
                border_col = C['text_accent']
                border_w = 2
                # glow behind selected button
                glow_s = pygame.Surface((btn_w + 20, btn_h + 20), pygame.SRCALPHA)
                glow_s.fill((*C['menu_accent'], 18))
                self.screen.blit(glow_s, (rect.x - 10, rect.y - 10))
            else:
                btn_col = C['card_bg']
                border_col = C['card_border']
                border_w = 1

            draw_rounded_rect(self.screen, btn_col, rect, radius=12,
                              border=border_w, border_color=border_col)

            # icon prefix
            icon_char = '\u25b6' if i == 0 else '\u2328'
            icon_surf = self.font_lg.render(icon_char, True, C['text'] if selected else C['text_dim'])
            self.screen.blit(icon_surf, (rect.x + 14, rect.y + 10))

            # main label
            lt = self.font_lg.render(label, True, C['text'] if selected else C['text_dim'])
            self.screen.blit(lt, (rect.x + 40, rect.y + 10))

            # sub-description
            dt_text = self.font_sm.render(desc, True, C['text_dim'])
            self.screen.blit(dt_text, (rect.x + 40, rect.y + 34))

            # selection indicator arrow
            if selected:
                arrow_x = rect.right - 24
                arrow_y = rect.centery
                bounce = math.sin(t * 5) * 3
                pygame.draw.polygon(self.screen, C['text_accent'], [
                    (arrow_x + bounce, arrow_y),
                    (arrow_x - 8 + bounce, arrow_y - 6),
                    (arrow_x - 8 + bounce, arrow_y + 6),
                ])

        # hint text
        hint_y = btn_manual_y + btn_h + 20
        hint = self.font_sm.render('\u2191\u2193 to select  |  ENTER or click to start', True, C['text_dim'])
        hr = hint.get_rect(center=(mid_x, hint_y))
        self.screen.blit(hint, hr)

        # credits
        credit = self.font_sm.render('PFAI Assignment \u2014 Spring 2024', True,
                                     (50, 45, 75))
        cr = credit.get_rect(center=(mid_x, height - 30))
        self.screen.blit(credit, cr)

        return (btn_ai_rect, btn_manual_rect)

    # ══════════════════════════════════════════════════════════════════════════
    #  DRAW: GAME OVER OVERLAY
    # ══════════════════════════════════════════════════════════════════════════
    def draw_game_over(self):
        # semi-transparent overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        mid_x = width // 2
        mid_y = height // 2

        # result card
        card_w, card_h = 380, 280
        card_rect = pygame.Rect(mid_x - card_w // 2, mid_y - card_h // 2,
                                card_w, card_h)
        draw_rounded_rect(self.screen, C['panel_bg'], card_rect, radius=16,
                          border=2, border_color=C['card_border'])

        w = self.world
        is_win = w.win

        # title
        result_text = 'VICTORY!' if is_win else 'GAME OVER'
        result_color = C['win'] if is_win else C['lose']
        rt = self.font_title.render(result_text, True, result_color)
        rr = rt.get_rect(center=(mid_x, mid_y - 90))
        self.screen.blit(rt, rr)

        # subtitle
        who = 'You' if self.play_mode == self.MODE_MANUAL else 'Agent'
        if is_win:
            sub_text = f'{who} grabbed the gold and returned home!'
        elif 'pit' in w.last_action:
            sub_text = f'{who} fell into a deadly pit...'
        elif 'eaten' in w.last_action:
            sub_text = f'{who} got eaten by the Wumpus!'
        else:
            sub_text = 'No safe moves remaining.'
        st = self.font_md.render(sub_text, True, C['text_dim'])
        sr = st.get_rect(center=(mid_x, mid_y - 45))
        self.screen.blit(st, sr)

        # stats
        stats = [
            f'Final Score: {w.score}',
            f'Total Moves: {w.moves}',
            f'Wumpus: {"Killed" if not w.wumpus_alive else "Alive"}',
            f'Gold: {"Collected" if w.gold_grabbed else "Missed"}',
        ]
        for i, s in enumerate(stats):
            st = self.font_md.render(s, True, C['text'])
            sr = st.get_rect(center=(mid_x, mid_y - 5 + i * 24))
            self.screen.blit(st, sr)

        # restart hint
        pulse = math.sin(self.time * 3) * 0.3 + 0.7
        hint_col = tuple(int(c * pulse) for c in C['text_accent'])
        hint = self.font_md.render('Press R to restart  |  ESC for menu', True, hint_col)
        hr = hint.get_rect(center=(mid_x, mid_y + 110))
        self.screen.blit(hint, hr)

    # ══════════════════════════════════════════════════════════════════════════
    #  MAIN LOOP
    # ══════════════════════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════════════════════
    #  MANUAL MODE — handle a player keyboard action and trigger effects
    # ══════════════════════════════════════════════════════════════════════════
    def _manual_action(self, action_fn):
        """Execute a manual action, update KB, log it, and trigger effects."""
        if self.world.over:
            return
        prev = self.world.last_action
        action_fn()
        # update KB so the grid reveals visited cells
        self.agent.kb.observe(self.world)
        self._log_action()
        self._trigger_effects()

    def _trigger_effects(self):
        """Spawn particles / shake on special events."""
        action = self.world.last_action
        if action == 'grabbed gold!':
            px, py = self.world.player_pos
            cx, cy = self.cell_center(px, py)
            self.particles.emit(cx, cy, C['gold'],
                                count=30, life=1.2, speed=60, size=4)
        elif action == 'killed wumpus!':
            for xx in range(grid_size):
                for yy in range(grid_size):
                    if self.world.grid[xx][yy].get('wumpus_was'):
                        cx, cy = self.cell_center(xx, yy)
                        self.particles.emit(cx, cy, C['wumpus'],
                                            count=25, life=1.0)
        elif 'pit' in action or 'eaten' in action:
            self.shake_amount = 12

    def run(self):
        menu_btn_rects = None  # tuple: (ai_rect, manual_rect)

        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.time += dt

            # ── events ──
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # ────────── MENU STATE ──────────
                    if self.state == self.STATE_MENU:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.menu_selection = 0
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.menu_selection = 1
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            mode = self.MODE_AI if self.menu_selection == 0 else self.MODE_MANUAL
                            self.new_game(mode)

                    # ────────── PLAY STATE ──────────
                    elif self.state == self.STATE_PLAY:
                        if self.play_mode == self.MODE_AI:
                            # AI mode controls
                            if event.key == pygame.K_SPACE:
                                self.auto = not self.auto
                            elif event.key == pygame.K_r:
                                self.new_game()
                            elif event.key == pygame.K_RIGHT and not self.auto:
                                if not self.world.over:
                                    self.agent.act()
                                    self._log_action()
                                    self._trigger_effects()
                            elif event.key == pygame.K_ESCAPE:
                                self.state = self.STATE_MENU
                        else:
                            # ── MANUAL mode controls ──
                            w = self.world
                            if event.key in (pygame.K_UP, pygame.K_w):
                                def _act():
                                    w.player_dir = Dir.UP
                                    w.move_forward()
                                self._manual_action(_act)
                            elif event.key in (pygame.K_DOWN, pygame.K_s):
                                def _act():
                                    w.player_dir = Dir.DOWN
                                    w.move_forward()
                                self._manual_action(_act)
                            elif event.key in (pygame.K_LEFT, pygame.K_a):
                                def _act():
                                    w.player_dir = Dir.LEFT
                                    w.move_forward()
                                self._manual_action(_act)
                            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                                def _act():
                                    w.player_dir = Dir.RIGHT
                                    w.move_forward()
                                self._manual_action(_act)
                            elif event.key == pygame.K_f:
                                # shoot arrow in current direction
                                self._manual_action(w.shoot)
                            elif event.key == pygame.K_g:
                                # grab gold
                                self._manual_action(w.grab_gold)
                            elif event.key == pygame.K_c:
                                # climb out (win if at 0,0 with gold)
                                if w.player_pos == (0, 0) and w.gold_grabbed:
                                    w.win = True
                                    w.over = True
                                    w.last_action = 'climbed out!'
                                    self._log_action()
                                    px, py = w.player_pos
                                    cx, cy = self.cell_center(px, py)
                                    self.particles.emit(cx, cy, C['win'],
                                                        count=40, life=1.5, speed=60, size=4)
                                else:
                                    w.last_action = 'can\'t climb (need gold at 0,0)'
                                    self._log_action()
                            elif event.key == pygame.K_r:
                                self.new_game()
                            elif event.key == pygame.K_ESCAPE:
                                self.state = self.STATE_MENU

                    # ────────── GAME OVER STATE ──────────
                    elif self.state == self.STATE_OVER:
                        if event.key == pygame.K_r:
                            self.new_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = self.STATE_MENU

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == self.STATE_MENU and menu_btn_rects:
                        ai_rect, manual_rect = menu_btn_rects
                        if ai_rect.collidepoint(event.pos):
                            self.new_game(self.MODE_AI)
                        elif manual_rect.collidepoint(event.pos):
                            self.new_game(self.MODE_MANUAL)

            # ── update ──
            if self.state == self.STATE_MENU:
                self.menu_time += dt

            elif self.state == self.STATE_PLAY:
                # auto-step agent (AI mode only)
                if self.play_mode == self.MODE_AI and self.auto and not self.world.over:
                    self.step_timer += dt * 1000
                    if self.step_timer >= AGENT_STEP_INTERVAL:
                        self.step_timer = 0
                        self.agent.act()
                        self._log_action()
                        self._trigger_effects()

                # transition to game over
                if self.world.over and self.state == self.STATE_PLAY:
                    self.state = self.STATE_OVER
                    # death particles
                    if not self.world.win:
                        px, py = self.world.player_pos
                        cx, cy = self.cell_center(px, py)
                        self.particles.emit(cx, cy, C['lose'],
                                            count=40, life=1.5, speed=80, size=4)

                # screen shake decay
                if self.shake_amount > 0:
                    self.shake_amount = max(0, self.shake_amount - self.shake_decay * dt * 10)

            # update particles
            self.particles.update(dt)

            # ── draw ──
            if self.state == self.STATE_MENU:
                menu_btn_rects = self.draw_menu()

            else:
                # apply screen shake
                shake_x = random.randint(-int(self.shake_amount),
                                         max(1, int(self.shake_amount)))
                shake_y = random.randint(-int(self.shake_amount),
                                         max(1, int(self.shake_amount)))

                self.screen.fill(C['bg'])
                original_clip = self.screen.get_clip()
                self.screen.set_clip(None)

                shake_surf = self.screen
                if self.shake_amount > 0.5:
                    shake_surf = pygame.Surface((width, height))
                    shake_surf.fill(C['bg'])
                    self.screen = shake_surf

                self.draw_grid()
                self.particles.draw(self.screen)
                self.draw_info_panel()

                if self.shake_amount > 0.5:
                    self.screen = pygame.display.get_surface()
                    self.screen.fill(C['bg'])
                    self.screen.blit(shake_surf, (shake_x, shake_y))

                if self.state == self.STATE_OVER:
                    self.draw_game_over()

                # mode indicator at bottom-left
                if self.state == self.STATE_PLAY:
                    if self.play_mode == self.MODE_AI:
                        mode_text = 'AI: AUTO' if self.auto else 'AI: PAUSED'
                        mode_col = C['safe_dot'] if self.auto else C['gold']
                    else:
                        mode_text = 'MANUAL'
                        mode_col = C['breeze']
                    pulse = math.sin(self.time * 4) * 0.2 + 0.8
                    col = tuple(int(c * pulse) for c in mode_col)
                    mt = self.font_sm.render(f'[{mode_text}]', True, col)
                    self.screen.blit(mt, (8, height - 22))

            pygame.display.flip()

    def _log_action(self):
        action = self.world.last_action
        if action and action != self.prev_action:
            move_num = self.world.moves
            self.action_log.append(f'#{move_num:02d} {action}')
            self.prev_action = action


if __name__ == '__main__':
    Game().run()