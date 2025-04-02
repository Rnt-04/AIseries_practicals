import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Grid parameters
grid_size = 8  # 8x8 grid
blast_radius = 2  # Radius in grid cells (Manhattan Distance)
W_e = 10  # Reward for hitting an enemy
W_f = 20  # Penalty for hitting a friendly

# Initialize positions
enemies = []
friendlies = []
mode = "placing"  # "placing" -> place units, "firing" -> fire artillery

# Manhattan Distance Function
def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Function to calculate explosion reward
def explosion_reward(x, y):
    enemies_hit = sum(manhattan_dist(ex, ey, x, y) <= blast_radius for ex, ey in enemies)
    friendlies_hit = sum(manhattan_dist(fx, fy, x, y) <= blast_radius for fx, fy in friendlies)
    return (W_e * enemies_hit) - (W_f * friendlies_hit)

# Function to update and draw grid
def update_plot():
    ax.clear()
    ax.set_xticks(range(grid_size + 1))
    ax.set_yticks(range(grid_size + 1))
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Draw enemies and friendlies
    for ex, ey in enemies:
        ax.scatter(ey + 0.5, grid_size - ex - 0.5, marker='x', color='red', s=100, label="Enemy")
    for fx, fy in friendlies:
        ax.scatter(fy + 0.5, grid_size - fx - 0.5, marker='o', color='blue', s=100, edgecolor="black", label="Friendly")
    
    ax.set_title("Place Units (Left: Enemy, Right: Friendly) - Press 'Start' to Fire")
    plt.draw()

# Mouse click event for placing units or firing
def on_click(event):
    global mode
    if event.inaxes is None:
        return
    
    grid_x = int(grid_size - event.ydata)  # Convert click to grid row
    grid_y = int(event.xdata)  # Convert click to grid column

    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:  # Ensure valid grid position
        if mode == "placing":
            if event.button == 1:  # Left-click: Place enemy
                enemies.append((grid_x, grid_y))
            elif event.button == 3:  # Right-click: Place friendly
                friendlies.append((grid_x, grid_y))
            update_plot()
        
        elif mode == "firing":
            reward = explosion_reward(grid_x, grid_y)
            ax.set_title(f"Artillery Fired at ({grid_x}, {grid_y}) - Reward: {reward}")
            plt.draw()

# Start firing mode
def start_firing(event):
    global mode
    mode = "firing"
    ax.set_title("Click on a grid cell to fire artillery!")
    plt.draw()

# Clear grid
def clear_grid(event):
    global enemies, friendlies, mode
    enemies = []
    friendlies = []
    mode = "placing"
    update_plot()

# Create interactive plot
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.15)
update_plot()

# Connect mouse event
fig.canvas.mpl_connect('button_press_event', on_click)

# Add "Start" button to fire artillery
ax_start = plt.axes([0.3, 0.02, 0.2, 0.05])
button_start = Button(ax_start, 'Start')
button_start.on_clicked(start_firing)

# Add "Clear" button
ax_clear = plt.axes([0.55, 0.02, 0.2, 0.05])
button_clear = Button(ax_clear, 'Clear')
button_clear.on_clicked(clear_grid)

plt.show()
