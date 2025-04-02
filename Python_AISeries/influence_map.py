import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Grid Parameters
grid_size = (8, 8)
max_influence = 100   # Max influence of a military unit
drop_off = 15         # Influence drop-off per unit distance
max_radius = 3        # Maximum influence radius

# Initialize positions of friendly and enemy forces
friendly_forces = []
enemy_forces = []

# Influence calculation function
def calculate_influence(grid_size, forces, max_influence, drop_off, max_radius):
    influence_map = np.zeros(grid_size)
    for fx, fy in forces:
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                dist = np.sqrt((fx - x) ** 2 + (fy - y) ** 2)
                if dist <= max_radius:
                    influence_map[x, y] += max(0, max_influence - drop_off * dist)
    return influence_map

# Function to update and plot the influence map
def update_plot():
    ax.clear()
    friendly_influence = calculate_influence(grid_size, friendly_forces, max_influence, drop_off, max_radius)
    enemy_influence = calculate_influence(grid_size, enemy_forces, max_influence, drop_off, max_radius)
    
    security_level = friendly_influence - enemy_influence
    
    ax.imshow(security_level, cmap='coolwarm', origin='upper', extent=[0, 8, 0, 8])
    ax.set_xticks(range(9))
    ax.set_yticks(range(9))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Mark friendly and enemy positions
    for fx, fy in friendly_forces:
        ax.scatter(fy + 0.5, 7 - fx + 0.5, marker='o', color='blue', s=100, edgecolor="black", label="Friendly Forces")
    
    for ex, ey in enemy_forces:
        ax.scatter(ey + 0.5, 7 - ex + 0.5, marker='x', color='red', s=100, label="Enemy Forces")
    
    ax.set_title("Influence Map and Security Level")
    ax.legend(["Friendly Forces", "Enemy Forces"], loc="upper right")
    plt.draw()

# Mouse click event to add forces
def on_click(event):
    if event.inaxes is not None:
        grid_x = int(7 - event.ydata)  # Convert plot coordinates to grid
        grid_y = int(event.xdata)
        if event.button == 1:  # Left-click: Add friendly force
            friendly_forces.append((grid_x, grid_y))
        elif event.button == 3:  # Right-click: Add enemy force
            enemy_forces.append((grid_x, grid_y))
        update_plot()

# Clear all forces
def clear_forces(event):
    global friendly_forces, enemy_forces
    friendly_forces = []
    enemy_forces = []
    update_plot()

# Create interactive plot
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.15)
update_plot()

# Connect mouse click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Add a clear button
ax_clear = plt.axes([0.4, 0.02, 0.2, 0.05])  # Button position
button_clear = Button(ax_clear, 'Clear')
button_clear.on_clicked(clear_forces)

plt.show()
