import numpy as np
import matplotlib.pyplot as plt

# Création d'une fonction pour un réseau de N fentes circulaires 2D
def N_circular_slits_2D(x, y, slit_radius, slit_distance, N):
    slits = 0
    for i in range(N):
        slits += np.where((x - (i - (N-1)/2) * slit_distance)**2 + y**2 <= slit_radius**2, 1, 0)
    return slits

# Paramètres du réseau de N fentes circulaires
slit_radius = 0.5
slit_distance = 3
N = 3

# Création d'une grille de points
x = np.arange(-10, 10, 0.05)
y = np.arange(-10, 10, 0.05)
X, Y = np.meshgrid(x, y)

# Calcul de la fonction pour un réseau de N fentes circulaires 2D
N_circular_slits = N_circular_slits_2D(X, Y, slit_radius, slit_distance, N)

# Calcul de la FFT 2D
fft_N_circular_slits = np.fft.fftshift(np.fft.fft2(N_circular_slits))

# Affichage de la fonction pour un réseau de N fentes circulaires 2D et sa FFT
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(N_circular_slits, extent=(x.min(), x.max(), y.min(), y.max()), origin='lower', cmap='gray')
plt.title(f'{N} Circular Slits Pattern')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(np.abs(fft_N_circular_slits), extent=(-1/(2*(x[1]-x[0])), 1/(2*(x[1]-x[0])), -1/(2*(y[1]-y[0])), 1/(2*(y[1]-y[0]))), origin='lower', cmap='viridis')
plt.title(f'FFT of {N} Circular Slits Pattern')
plt.colorbar()

plt.tight_layout()
plt.show()
