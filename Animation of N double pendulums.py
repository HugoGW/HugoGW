import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

# Length of pendulums (m)
L1 = 1.0
L2 = 1.0

# Mass of pendulums (kg)
m1 = 1.0
m2 = 1.0

# Gravitational acceleration (en m/s^2)
g = 9.81

# Function that solve ODE using odeint
def solve_ODE(equation, f0, t_values, colonne):
    solution = odeint(equation, f0, t_values)
    f_values = solution[:, colonne]
    return f_values

# Function representing the differential equations for the double pendulum.
def Eq_DP(y, t):
    theta1, theta1_dot, theta2, theta2_dot = y

    # Differential equations of θ1 and θ2
    theta1_double_dot = (m2 * g * np.sin(theta2) * np.cos(theta1 - theta2) - m2 * np.sin(theta1 - theta2) * (L1 * theta1_dot ** 2 * np.cos(theta1 - theta2) + L2 * theta2_dot ** 2) - (m1 + m2) * g * np.sin(theta1)) / (L1 * (m1 + m2 * np.sin(theta1 - theta2) ** 2))
    theta2_double_dot = ((m1 + m2) * (L1 * theta1_dot ** 2 * np.sin(theta1 - theta2) - g * np.sin(theta2) + g * np.sin(theta1) * np.cos(theta1 - theta2)) + m2 * L2 * theta2_dot ** 2 * np.sin(theta1 - theta2) * np.cos(theta1 - theta2)) / (L2 * (m1 + m2 * np.sin(theta1 - theta2) ** 2))

    return [theta1_dot, theta1_double_dot, theta2_dot, theta2_double_dot]

N_pend = 20  # Number of pendulum

# Initial conditions
dθ1 = np.radians(0.0001)
dθ2 = np.radians(0.0)
dω1 = np.radians(0.0)
dω2 = np.radians(0.0)
θ1_0 = np.radians(180)
θ2_0 = np.radians(90)
ω1_0 = np.radians(0.0)
ω2_0 = np.radians(0.0)
θ_init = []

for i in range(N_pend):
    θ_init.append([θ1_0 + i*dθ1, ω1_0 + i*dω1, θ2_0 + i*dθ2, ω2_0 + i*dω2])

# Time interval for the simulation
t_start = 0.0
t_end = 15.0
t_values = np.arange(t_start, t_end, 0.01)

# Solving the differential equations for the n pendulums.
θ_1 = [solve_ODE(Eq_DP, θ_0, t_values, 0) for θ_0 in θ_init]
θ_2 = [solve_ODE(Eq_DP, θ_0, t_values, 2) for θ_0 in θ_init]

# Cartesian coordinates for each pendulum
x1 = [L1 * np.sin(θ) for θ in θ_1]
y1 = [-L1 * np.cos(θ) for θ in θ_1]
x2 = [x + L2 * np.sin(θ) for x, θ in zip(x1, θ_2)]
y2 = [y - L2 * np.cos(θ) for y, θ in zip(y1, θ_2)]

# Animation of the n double pendulums
fig, ax = plt.subplots()
lines = [plt.plot([], [], lw=2)[0] for _ in range(N_pend)]

def init():
    for line in lines:
        ax.set_xlim((-L1 - L2)*1.1, (L1 + L2)*1.1)
        ax.set_ylim((-L1 - L2)*1.1, (L1 + L2)*1.1)
        ax.set_aspect('equal')
        line.set_data([], [])
    return lines

def animate(i):
    for j in range(N_pend):
        lines[j].set_data([0, x1[j][i], x2[j][i]], [0, y1[j][i], y2[j][i]])
    return lines

ani = FuncAnimation(fig, animate, frames=len(t_values), init_func=init, interval=1)
plt.title(f'Animation of {N_pend} double pendulum(s)')
plt.legend()
plt.show()
