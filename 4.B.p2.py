import numpy as np
import matplotlib.pyplot as plt
import math
from math import sin, cos, pi, exp, floor
from scipy import constants
import scipy.constants as sc

Nptos =500

Ez = np.zeros(Nptos)
Hy = np.zeros(Nptos)
E0 = 1  # Amplitud de la onda inicial
epsi = np.zeros(Nptos)
mu = np.zeros(Nptos)
V = constants.c
dt = 0.001e-9
dx = 2*dt*V
# cambio de epsilon del material, añadiendo las nuevas capas antireflejo
epsi[0:237]=sc.epsilon_0
epsi[237:244] = sc.epsilon_0*((12)**1/2)
epsi[244:257] = 12*sc.epsilon_0
epsi[257:264] = sc.epsilon_0*((12)**1/2)
epsi[264:Nptos] = sc.epsilon_0

##################################################
#Para hallar la reflexión y transmision de la onda
# Impedancias intrínsecasde de los medios
I1 = (sc.mu_0/sc.epsilon_0)**(1/2)
I2 = (sc.mu_0/(12*sc.epsilon_0))**(1/2)
I3 = (sc.mu_0/sc.epsilon_0)**(1/2)

# Reflexiones
R12 = (I2-I1)/(I2+I1)
R23 = (I3-I2)/(I3+I2)
#Transmisiones
T12 = (2*I2)/(I2+I1) 
T23 = (2*I3)/(I3+I2)  
# Transmision total teórica
Trans = T12*T23
#################################################
w=10E9#frecuencia
Ttotal = floor(1/(dt*w)) 
mult=7
#################################################
# para condicionar los bordes mas abajo
left = [0, 0]
right = [0, 0]

#Implementación del método
for i in range(0, mult*Ttotal):
    
    for j in range(1, Nptos):
        Ez[j] = Ez[j] + (dt/(epsi[j]*dx))*(Hy[j] - Hy[j - 1])  
    # onda
    if i < 151:
        onda = sin(2*pi*w*dt*i)
    Ez[0] = onda
    # volver bordes absorbentes
    if i > 151:
        Ez[0] = left.pop(0)
        left.append(Ez[1])
        Ez[Nptos - 1] = right.pop(0)
        right.append(Ez[Nptos - 2])
    
    for j in range(Nptos - 1):
        Hy[j] = Hy[j] + (dt/(sc.mu_0*dx)) * (Ez[j+1] - Ez[j])
#####################################################
#Grafica
    plt.plot(Ez)
    plt.plot([237, 237],[-1.5, 1.5])
    plt.plot([264, 264],[-1.5, 1.5])
    plt.plot([244, 244],[-1.5, 1.5])
    plt.plot([257, 257],[-1.5, 1.5])
    plt.ylabel('Campo eléctrico [V/m]')
    plt.xlabel('Posición [mm]')
    plt.xlim(0, Nptos)
    plt.ylim(-1.6, 1.6)
    plt.pause(0.0001)
    plt.show()

#####################################################       
# amplitud de salida
Newhout = abs(min(Ez[264.5:Nptos]))

print("Solo se transmitió",round(Newhout*100, 2),"% de la onda inicial, lo que deja como conclusión el mejorar los resultados colocando más capas hasta que no se refleje practicamente. Igualmente este resultado tiene como causa de error principal el no poder escribir numeros decimales en los intervalos de definición para los distintos epsilon de los materiales") 