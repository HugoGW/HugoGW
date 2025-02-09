import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Paramètres de l'onde spiralante
def gravitational_wave(x, y, t, center_x=0, center_y=0, wavelength=2, speed=1, spiral_factor=0.1):
    # Calcul des coordonnées polaires (distance et angle par rapport au centre)
    r = np.sqrt((x - center_x)**2 + (y - center_y)**2)  # Distance par rapport au centre
    theta = np.arctan2(y - center_y, x - center_x)  # Angle polaire
    
    # Simuler une onde qui se propage en spirale
    wave = np.sin(2 * np.pi * (r - speed * t) / wavelength) * np.cos(spiral_factor * t + theta)
    return wave

# Paramètres de l'orbite binaire
def binary_orbit(t, orbit_radius=1, orbital_speed=0.1):
    # Définir une orbite circulaire pour deux objets
    angle = orbital_speed * t
    x1 = orbit_radius * np.cos(angle)
    y1 = orbit_radius * np.sin(angle)
    
    # L'autre objet se déplace en orbite opposée
    x2 = -x1
    y2 = -y1
    return x1, y1, x2, y2

# Création du maillage
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
X, Y = np.meshgrid(x, y)
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("", fontsize=20, color='white', pad=15)  # Titre vide au début
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Initialisation de la grille
grid_lines = ax.quiver(X, Y, np.zeros_like(X), np.zeros_like(Y), color='cyan')

# Points représentant les étoiles
star1, = ax.plot([], [], 'wo', markersize=10)  # Etoile 1 (point blanc)
star2, = ax.plot([], [], 'wo', markersize=10)  # Etoile 2 (point blanc)

# Le texte du titre
title_text = "Hugo Alexandre"
current_title = ""

# Intervalle pour l'apparition des lettres (tous les 5 frames pour ralentir l'effet)
def update(frame):
    global current_title

    # Mise à jour du titre lettre par lettre tous les 5 frames
    if frame % 5 == 0 and len(current_title) < len(title_text):
        current_title += title_text[len(current_title)]
        ax.set_title(current_title, fontsize=30, color='white', pad=15)  # Augmenté la taille de la police à 30

    # Mise à jour de l'onde
    Z = gravitational_wave(X, Y, frame * 0.1)  # Mise à jour de l'onde à chaque frame
    U = np.cos(Z)  # Composante U des vecteurs
    V = np.sin(Z)  # Composante V des vecteurs
    grid_lines.set_UVC(U, V)  # Mise à jour des vecteurs du quiver
    
    # Mise à jour des positions des étoiles en orbite
    x1, y1, x2, y2 = binary_orbit(frame)
    star1.set_data(x1, y1)  # Position de la première étoile
    star2.set_data(x2, y2)  # Position de la deuxième étoile
    
    return grid_lines, star1, star2

# Sauvegarde de l'animation
save_path = r'P:\Python\gravitational_waves_spiral_with_stars.gif'
ani = animation.FuncAnimation(fig, update, frames=150, interval=50, blit=False)
ani.save(save_path, writer="pillow", fps=20)
plt.close()
