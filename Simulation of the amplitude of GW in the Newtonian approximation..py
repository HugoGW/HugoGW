import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Binary parameters and physical parameters
M_0 = 2*10**(30)
m1 = 3*M_0 # mass of the first star in solar mass
m2 = 3*M_0 # mass of the second star in solar mass
t_c = 10 # coalescence time
f_0 = 100 # orbit frequency
G = 6.67*10**(-11)
c = 299792458
M = (m1 * m2 / (m1 + m2))**(3/5) * (m1 + m2)**(2/5)  # Chirp mass
R = 500*3.086*10**(19) # distance of observation


def f_og(f_0, t, t_c):
    return f_0*(1-(t-t_c))**(-5/8)

#Function that calculates the amplitude of the gravitational wave
def h(t):
    return 4*(G**(5/3)/c**4)*M**(5/3)/R*(t_c - t)**(-3/5)*np.sin(np.pi*f_og(f_0, t, t_c)*(t-t_c))


# Calculation of the amplitude for times from 0 to tc
t = np.linspace(0, t_c-t_c/75, 100000)
h_t = h(t)

fig, ax = plt.subplots()
Tdata, Hdata = [], []
line, = ax.plot([], [])

def init():
    ax.set_xlim(0, t_c-t_c/75)
    ax.set_ylim(-4*(G**(5/3)/c**4)*M**(5/3)/R*(t_c/75)**(-3/5), 4*(G**(5/3)/c**4)*M**(5/3)/R*(t_c/75)**(-3/5))
    return line,

def update(frame):
    T = frame*50
    H_T = h(T)
    Tdata.append(T)
    Hdata.append(H_T)
    line.set_data(Tdata, Hdata)
    line.set_lw(2) # Increase the line thickness for better visibility
    return line,

ani = FuncAnimation(fig, update, frames=t, init_func=init, blit=True, interval=1)

plt.xlabel('time (s)', fontsize = 16)
plt.ylabel(r"Amplitude of the GW $h(t)$", fontsize = 16)
plt.title(r"Amplitude of the GW in the Newtonian approximation at $R=100 Mpc$", fontsize = 18)
plt.show()