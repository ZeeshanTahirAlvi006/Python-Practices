import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

GRID_SIZE = 100
grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.8, 0.2]).astype(int)
glider =np.array([[0,1,0],[0,0,1,],[1,1,1]])
grid[2:5,2:5] = glider
print(grid[2:5,2:5])
fig, ax = plt.subplots(figsize =(6,6)) #set the size of the figure
img = ax.imshow(grid,cmap='binary',interpolation='nearest')
def animate(frame):
    global grid
    grid = update_grid(grid)
    img.set_data(grid)
    return [img]

def update_grid(grid):
    neighbors = (
        np.roll(grid,1,axis = 0 ) +
    np.roll(grid,-1,axis = 0) +
    np.roll(grid,1,axis = 1) +
    np.roll(grid, -1, axis = 1) +
    np.roll(np.roll(grid,1,axis = 0),1,axis = 1) +
    np.roll(np.roll(grid,1,axis = 0),-1,axis = 1)+
    np.roll(np.roll(grid,-1,axis = 0),1,axis = 1)+
    np.roll(np.roll(grid,-1,axis = 0),-1,axis = 1)
    )
    next_grid = (neighbors == 3) | ((grid == 1) & (neighbors == 2))
    return next_grid.astype(int)
ani = animation.FuncAnimation(fig,animate,frames = 200,interval = 100,blit = True)
plt.show()