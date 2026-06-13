# Wumpus World — AI Explorer: Short Report

---

## 1. Explanation of Classes

The project is organized into **seven** main classes, each handling a distinct responsibility:

| Class | Lines | Purpose |
|---|---|---|
| **`Particle`** | 70–95 | Represents a single visual particle (position, velocity, color, lifetime). Updates its physics each frame and fades out over time. |
| **`ParticleSystem`** | 98–111 | Manages a collection of `Particle` objects — emitting bursts of particles at a given location, updating them, and drawing surviving particles each frame. |
| **`World`** | 117–261 | Core **game logic** layer. Maintains the 4×4 grid, places the Wumpus, pits, and gold randomly, handles movement, shooting the arrow, grabbing gold, and updates environmental percepts (stench & breeze). Tracks score, move count, and win/loss state. |
| **`KB`** (Knowledge Base) | 267–335 | The agent's **internal model** of the world. For every cell it records whether the cell has been visited, is safe, or might contain the Wumpus/pit. It applies logical inference (see §2 below) to deduce safe and dangerous cells from percept observations. |
| **`Agent`** | 341–419 | The **AI controller**. Each call to `act()` observes the current cell, grabs gold if present, plans a path via BFS to the nearest safe-unvisited cell (or back to the start after grabbing gold), and can shoot the Wumpus if its location has been uniquely inferred. |
| **`Game`** | 456–1105 | The **main application** class. Initializes Pygame, manages three game states (Menu → Play → Game Over), orchestrates the render loop (grid, sidebar info panel, particles, overlays), handles keyboard/mouse input, and auto-steps the agent at a configurable interval. |
| **`Dir`** (Enum) | 63–64 | Simple directional enum: `UP`, `RIGHT`, `DOWN`, `LEFT` — used to track the player's facing direction. |

### Standalone Helper Functions

- **`lerp_color`** — Linear color interpolation for smooth visual transitions.
- **`draw_glow_circle`** — Renders multi-ring glow effects around entities (player, gold, Wumpus).
- **`draw_rounded_rect`** — Draws styled rounded rectangles used throughout the UI.
- **`ease_in_out`** — Smooth easing curve for animations.

---

## 2. AI Logic Used

### 2.1 Knowledge-Based Reasoning

The `KB` class implements a **propositional knowledge-base agent** inspired by the classic Wumpus World formulation from Russell & Norvig's *AI: A Modern Approach*:

1. **Observation** (`KB.observe`): When the agent visits a cell, it marks the cell safe and records whether stench or breeze is present.
2. **Constraint propagation**:
   - If a visited cell has **no stench**, all its neighbors are marked `wumpus_p = False` (cannot contain the Wumpus).
   - If a visited cell has **no breeze**, all its neighbors are marked `pit_p = False` (cannot contain a pit).
   - Any cell with both `wumpus_p = False` and `pit_p = False` is inferred **safe**.
3. **Wumpus localization** (`KB.infer_wumpus`): The agent collects all stench-bearing visited cells and intersects the sets of their unvisited neighbors that still have `wumpus_p = True`. When the intersection narrows to a **single candidate**, the Wumpus location is uniquely determined, enabling a targeted shot.

### 2.2 Pathfinding — BFS

The `Agent.bfs` method performs **Breadth-First Search** over the grid, restricted to cells the KB has marked safe. This guarantees:

- **Shortest safe path** to the nearest unexplored safe cell during exploration.
- **Optimal return route** back to (0, 0) after grabbing the gold.

### 2.3 Decision Cycle (`Agent.act`)

Each step the agent follows this priority order:

```
1. Observe current cell → update KB
2. Grab gold if present
3. If gold is grabbed → BFS to (0,0) → win on arrival
4. Follow any existing planned path
5. Attempt to shoot Wumpus (if uniquely located & adjacent)
6. BFS to nearest safe-unvisited cell → explore
7. If no safe moves remain → give up
```

This produces a cautious, knowledge-driven agent that never enters a cell it hasn't proven safe.

---

## 3. Challenges Faced

| Challenge | Description |
|---|---|
| **Random placement conflicts** | Ensuring the Wumpus, pits, and gold never overlap with each other or the start cell required careful placement loops with validity checks. |
| **Correct percept propagation** | Stench and breeze must be recalculated globally after the Wumpus is killed; missing this caused stale percepts and incorrect inferences. |
| **Wumpus inference edge cases** | The set-intersection logic for locating the Wumpus can produce an empty set if stench data is insufficient, requiring the agent to gracefully fall back to exploration. |
| **BFS restricted to safe cells** | If safe cells don't form a connected path to a goal, the agent can become stuck. Handling this "no safe moves" dead-end without crashing required an explicit termination condition. |
| **Screen shake & rendering** | Applying screen shake required rendering to an offscreen surface and blitting with an offset; directly moving draw calls caused visual artifacts. |
| **Particle lifecycle** | Particles that aren't cleaned up each frame cause memory growth and frame-rate drops; the list-comprehension filter in `ParticleSystem.update` resolved this. |

---

## 4. Learning Outcomes

1. **Knowledge-Based Agents**: Gained practical experience building an agent that maintains an internal knowledge base, applies logical inference rules, and makes decisions based on partial observability — a core concept in AI.

2. **Search Algorithms (BFS)**: Implemented BFS for shortest-path planning within a constrained graph (only safe cells), reinforcing understanding of graph search applied to real-time agent navigation.

3. **Propositional Inference**: Learned how simple constraint propagation (eliminating possibilities based on absence of percepts) can substitute for a full SAT solver in small domains.

4. **Game Architecture**: Practiced structuring a game into cleanly separated layers — world logic, AI agent, knowledge base, and rendering — following the Model–View–Controller pattern.

5. **Pygame Rendering Techniques**: Explored glow effects, particle systems, rounded-rectangle UI cards, screen-shake feedback, and animation pulsing, all of which contribute to a polished user experience.

6. **State Machine Design**: Managed three distinct game states (Menu, Play, Game Over) with clean transitions, reinforcing finite-state-machine design in interactive applications.

7. **Debugging AI Agents**: Learned to use an action log and visual KB overlays (safe dots, danger dots) to trace and debug agent decisions in real time — an essential skill for AI development.

---

> **Tools & Libraries**: Python 3, Pygame, standard library modules (`random`, `math`, `sys`, `collections.deque`, `enum`).
>
> **Source File**: `neon_wumpus.py` (1 109 lines)
