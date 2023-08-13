import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

# Length of pendulum (m)
L = 10

# Mass of pendulum (kg)
m = 28.0

# Gravitational acceleration (m/s^2)
g = 9.81

# Seconds in a day
T = 100

# pulsation of Earth's rotation
Ω = 2*np.pi/T

# Latitude of the pendulum
l = np.radians(-45)

# Pulsation of the pendulum
ω0 = np.sqrt(g/L)

# Function that solve ODE using odeint
def solve_ODE(equation, f0, t_values, colonne):
    solution = odeint(equation, f0, t_values)
    f_values = solution[:, colonne]
    return f_values

# Function representing the differential equations for the pendulum.
def Eq_DP(y, t):
    θ, dθdt, φ, dφdt = y

    # Differential equations of θ and φ
    
    d2θdt2 = 2*Ω*np.sin(l)*np.sin(θ)*np.cos(θ)*dφdt - 2*Ω*np.sin(φ)*np.sin(θ)**2*np.cos(l)*dφdt - ω0**2*np.sin(θ) + np.sin(θ)*np.cos(θ)*dφdt**2
    
    d2φdt2 = (-2*Ω*np.sin(l)*np.cos(θ)*dθdt + 2*Ω*np.sin(φ)*np.sin(θ)*np.cos(l)*dθdt - 2*np.cos(θ)*dθdt*dφdt)/np.sin(θ)
    
    return [dθdt, d2θdt2, dφdt, d2φdt2]

# Initial conditions
θ_0 = np.radians(60)
φ_0 = np.radians(0.0)
dθdt_0 = np.radians(0.0)
dφdt_0 = np.radians(0.0)
initial_conditions = [θ_0, φ_0, dθdt_0, dφdt_0]

# Time interval for the simulation
t_start = 0.0
t_end = 60
t_values = np.arange(t_start, t_end, 0.05)

# Solving the differential equations for the pendulum.
θ = solve_ODE(Eq_DP, initial_conditions, t_values, 0)
φ = solve_ODE(Eq_DP, initial_conditions, t_values, 2)

# Cartesian coordinates for the pendulum
x = L*np.sin(θ)*np.cos(φ)
y = L*np.sin(θ)*np.sin(φ)
z = -L*np.cos(θ)

# Animation function
def animate(i):
    ax.clear()
    ax.set_xlim([-L, L])
    ax.set_ylim([-L, L])
    ax.set_zlim([-L, 0])
    ax.plot(x[:i], y[:i], -1.1*L, color='blue')
    ax.scatter(x[i], y[i], z[i], color='red', marker='o', s=50)
    ax.plot([0, x[i]], [0, y[i]], [0, z[i]], color='black', linewidth=1)  # adding the rope
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Foucault\'s Pendulum Motion in 3D at latitude of {l*180/np.pi}°')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

# Create a 3D figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Animate the trajectory
ani = FuncAnimation(fig, animate, frames=len(t_values), interval=1)

plt.show()
