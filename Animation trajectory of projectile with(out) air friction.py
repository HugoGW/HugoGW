import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint


# Initial parameters
α = 0.0003718994604243878  # Friction coefficient (/s)
h = 10  # Initial height (m)
v_0 = 100  # Initial velocity (m/s)
theta = 45 # Angle of launch (°)
θ = theta * np.pi/180 # Angle of launch (rad)
g = 9.81  # Acceleration due to gravity (m/s²)


# Function to calculate the x and y coordinates at each moment t
def motion_ff(t, h, v_0, alpha):
    g = 9.81  
    v_0x = v_0 * np.cos(θ)
    v_0y = v_0 * np.sin(θ)
    x = v_0x * t
    y = h + v_0y * t - 0.5 * g * t**2
    return x, y

# Differential equation of motion for x and y (by considering the fluid friction of the air)

def X_friction(x, t):
    dx2dt2 = [x[1], -α * x[1]**2]
    return dx2dt2

def Y_friction(y, t):
    dy2dt2 = [y[1], -α * y[1]**2 - g]
    return dy2dt2


# Differential equation solving function
def solve_ODE(equation, f0, t_values):
    """
    Solve a second-order differential equation of the form f(y", y', y) = 0 with initial conditions y(0) = y0[0] and y'(0) = y0[1]

    Args:
        equation (function): The function representing the differential equation f(y", y', y) = 0.
f0 (list): The initial conditions [y(0), y'(0)].
t_values (array): The values of t for which to solve the equation.

    Returns:
        array: The values of y(x) obtained by solving the differential equation..
    """


    solution = odeint(equation, f0, t_values)
    f_values = solution[:, 0]
    return f_values

x0 = [0, v_0*np.cos(θ)]  # Initial conditions for x
y0 = [h, v_0*np.sin(θ)]  # Initial conditions for y

total_time = (v_0*np.sin(θ) + np.sqrt((v_0*np.sin(θ))**2 + 2*g*h))/g  # total time of flight

t = np.arange(0, total_time, 0.1)

# Calculation of the coordinates x and y at each moment.
x_ff, y_ff = motion_ff(t, h, v_0, θ)

# Solving the differential equation using the function solve_ODE.
x_friction = solve_ODE(X_friction, x0, t)
y_friction = solve_ODE(Y_friction, y0, t)

# Creating the figure and axis.
fig, ax = plt.subplots()
line1, = plt.plot([], [], 'ro', lw=2, color = 'blue', label='freefall')
line2, = plt.plot([], [], 'ro', lw=2, color = 'red', label='fluid friction')
ax.set_title('Projectile')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.set_xlim(0, max(x_ff))
ax.set_ylim(0, max(y_ff) * 1.5)
ax.grid(True)
ax.set_aspect('equal', adjustable='box')

# Initialisation of the trajectory
point1, = ax.plot([], [], 'ro', markersize=5, color = 'blue')
trail1, = ax.plot([], [], 'r', lw=1, color = 'blue')

point2, = ax.plot([], [], 'ro', markersize=5, color = 'red')
trail2, = ax.plot([], [], 'r', lw=1, color = 'red')

# Animation initialization function.
def init1():
    point1.set_data([], [])
    trail1.set_data([], [])
    return point1, trail1

def init2():
    point2.set_data([], [])
    trail2.set_data([], [])
    return point2, trail2

# Function to update the trajectory at each frame.
def animate1(frame):
    x_data1 = x_ff[frame]
    y_data1 = y_ff[frame]
    x_trail1 = x_ff[:frame]
    y_trail1 = y_ff[:frame]
    point1.set_data(x_data1, y_data1)
    trail1.set_data(x_trail1, y_trail1)
    return point1, trail1

def animate2(frame):
    x_data2 = x_friction[frame]
    y_data2 = y_friction[frame]
    x_trail2 = x_friction[:frame]
    y_trail2 = y_friction[:frame]
    point2.set_data(x_data2, y_data2)
    trail2.set_data(x_trail2, y_trail2)
    return point2, trail2

# Création of the animation
ani_ff = FuncAnimation(fig, animate1, frames=len(x_ff), init_func=init1, interval = 1)
ani_friction = FuncAnimation(fig, animate2, frames=len(x_friction), init_func=init1, interval = 1)

plt.legend()

# Displaying the animation.
plt.show()
