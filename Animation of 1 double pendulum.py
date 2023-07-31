import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

# Constantes physiques
G = 9.81  # Accélération due à la gravité (m/s^2)
L1 = 1.0  # Longueur du premier pendule (m)
L2 = 1.0  # Longueur du second pendule (m)
M1 = 1.0  # Masse du premier pendule (kg)
M2 = 1.0  # Masse du second pendule (kg)

# Fonction décrivant les équations du mouvement du double pendule
def double_pendulum_equations(t, state):
    theta1, omega1, theta2, omega2 = state

    dtheta1_dt = omega1
    dtheta2_dt = omega2

    delta_theta = theta2 - theta1
    domega1_dt = (M2 * G * np.sin(theta2) * np.cos(delta_theta) - M2 * np.sin(delta_theta) * (L1 * omega1**2 * np.cos(delta_theta) + L2 * omega2**2) - (M1 + M2) * G * np.sin(theta1)) / (L1 * (M1 + M2 * np.sin(delta_theta)**2))
    domega2_dt = ((M1 + M2) * (L1 * omega1**2 * np.sin(delta_theta) - G * np.sin(theta2) + G * np.sin(theta1) * np.cos(delta_theta)) + M2 * L2 * omega2**2 * np.sin(delta_theta) * np.cos(delta_theta)) / (L2 * (M1 + M2 * np.sin(delta_theta)**2))

    return dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt

# Conditions initiales (angles et vitesses angulaires)
def CI(theta1_0, theta2_0, omega1_0, omega2_0):
    initial_state = [theta1_0, omega1_0, theta2_0, omega2_0]
    return initial_state

# Intervalle de temps pour l'intégration numérique
t_span = [0, 10]  # Temps initial et final (s)

# Résolution numérique des équations du mouvement à l'aide de scipy.integrate.solve_ivp
solution1 = solve_ivp(double_pendulum_equations, t_span, CI(2*np.pi/3, np.pi, 0, 0), t_eval=np.linspace(t_span[0], t_span[1], 1000))

# Fonction d'animation
def animate_pendulum1(i):
    x1 = L1 * np.sin(solution1.y[0, i])
    y1 = -L1 * np.cos(solution1.y[0, i])
    x2 = x1 - L2 * np.sin(solution1.y[2, i])
    y2 = y1 + L2 * np.cos(solution1.y[2, i])

    pendulum1.set_data([0, x1, x2], [0, y1, y2])
    return pendulum1,


# Initialisation de la figure
fig, ax = plt.subplots()
ax.set_xlim(-L1 - L2, L1 + L2)
ax.set_ylim(-L1 - L2, L1 + L2)
ax.set_aspect('equal')
ax.set_title('Double Pendulum Animation')

# Dessin du pendules
pendulum1, = ax.plot([], [], lw=2, color ='blue')


# Création de l'animation
ani1 = FuncAnimation(fig, animate_pendulum1, frames=len(solution1.t), interval=5, blit=True)

# Affichage de l'animation
plt.show()
