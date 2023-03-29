import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

print("2D heat equation solver")

plate_length = 5
gridpoints  = 500
max_iter_time = 50

alpha = 2 #thermal diffusivity
delta_x = 1

delta_t = (delta_x ** 2)/(4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j)
u = np.empty((max_iter_time, gridpoints, gridpoints))

# Initial condition everywhere inside the grid
u_initial = 0

# Boundary conditions
#u_top = 100.0
#u_left = 0.0
#u_bottom = 0.0
#u_right = 0.0

# Set the initial condition
u.fill(u_initial)

# Set the boundary conditions
#u[:, (plate_length-1):, :] = u_top
#u[:, :, :1] = u_left
#u[:, :1, 1:] = u_bottom
#u[:, :, (plate_length-1):] = u_right

# Set the intitial conditions

def set_intial_circle(u, r, T):
    for xcord in range(u.shape[1]):
        for ycord in range(u.shape[2]):
            x = (xcord - gridpoints//2) * plate_length/gridpoints
            y =  (ycord - gridpoints//2) * plate_length/gridpoints
            # If the point is in the circle
            if np.sqrt(x**2 + y**2)<=r:
                u[0,xcord,ycord] = T
    return u

def calculate(u):
    for k in range(0, max_iter_time-1, 1):
        for i in range(1, gridpoints-1, delta_x):
            for j in range(1, gridpoints-1, delta_x):
                u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]

    return u

def plotheatmap(u_k, k):
    # Clear the current plot figure
    plt.clf()

    plt.title(f"Temperature at t = {k*delta_t:.3f} unit time")
    plt.xlabel("x")
    plt.ylabel("y")

    # This is to plot u_k (u at time-step k)
    plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar()

    return plt

# Init the circle
u = set_intial_circle(u,1,100)

# Do the calculation here
u = calculate(u)

plt.pcolormesh(u[20], cmap=plt.cm.jet, vmin=0, vmax=100)
plt.show()

def animate(k):
    plotheatmap(u[k], k)

anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=max_iter_time, repeat=False)
anim.save("heat_equation_solution.gif")

print("Done!")
