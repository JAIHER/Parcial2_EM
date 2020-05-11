import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi, floor
import scipy.constants as sc

Nptos =500

Ez = np.zeros(Nptos)
Hy = np.zeros(Nptos)
E0 = 1  # Amplitud de la onda inicial
epsi = np.zeros(Nptos)
mu = np.zeros(Nptos)
V = sc.c
dt = 0.001e-9
dx = 2*dt*V
# cambio de epsilon del material
epsi[0:244] = sc.epsilon_0
epsi[244:257] = 12*sc.epsilon_0
epsi[257:Nptos] = sc.epsilon_0

w=10E9#frecuencia

# para condicionar los bordes mas adelante
left = [0, 0]
right = [0, 0]
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
Ttotal = floor(1/(dt*w)) 
mult=7
#################################################
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
    plt.plot([244, 244],[-1.5, 1.5])
    plt.plot([257, 257],[-1.5, 1.5])
    plt.ylabel('Campo eléctrico [V/m]')
    plt.xlabel('Posición [mm]')
    plt.xlim(0, Nptos)
    plt.ylim(-1.5, 1.5)
    plt.pause(0.0001)
    plt.show()

# amplitud de salida
hout = abs(min(Ez[257:Nptos])/E0)

# diferencia con la onda transmitida
#Error porcentual
Ep= abs(((hout-Trans)/Trans))*100
#Totalidad
Ea = round(Ep, 3)

print("Se halló un error del", Ep, "% y se transmitio el",round(hout*100, 2),"%.")
print("Se puede decir a partir de los resultados y de nuestra premisa de que necesitamos que nos proteja una antena y a la vez deje transmitir eficazmente la señal opino que el material a pesar de no responder exageradamente mal, deja igual bastante cabida a que seguramente podría existir o crearse otro material mejor y mas eficaz a la hora de transmitir mayor porcentaje de la onda.")
print("Pdta, tuve que cambiar la escala de graficación, cuando se lo mostré en la sustentación estaba en cm, y ahora en mm, tuve que hacerlo debido a que variar la velocidad de progpagación que le mostré ese día no se me facilitó y con esta escala se aprecia mucho mejor el efecto que queremos (A pesar de no ser tan rápida como quería que fuera), de paso funciona mejor para el punto b")