# Engineering 100 Final Flying Backpack Model

import matplotlib.pyplot as plt
import time
import math
from math import *

# variables
temperature = 20  # Celsius
pressure = 101325  # Pascals

mylar_d = 1400  # mylar density in kg/m^3
air_d = 1.204  # air density in kg/m^3 at 20 degrees Celsius

hydrogen_d = 0.0887  # density of hydrogen gas in kg/m^3
helium_d = 0.1761  # density of helium gas in kg/m^3

cd_sphere = 0.47  # coefficient of drag for a sphere

speed_walk_m = 1.395  # average walking speed of a man age 20-29 in m/s
speed_walk_w = 1.408  # average walking speed of a woman age 20-29 in m/s

battery_capacity = 0  # in Amp hours
idle_power_draw = 0.0372 + 3.1  # taking into account computing power and stereo camera vision system with 12 cameras

optimal_battery_life = 8  # hours

# masses that are constant
antenna = 0
motors = 0
electronics = 0


# [function for calculating mass of components of backpack here]


# returns radius of a balloon required to lift a certain mass
def size_of_balloon(pA, pG, mass):
    radius = pow(((3 * mass) / (4 * math.pi * (pA - pG))), 1 / 3)
    # volume = (4 / 3) * math.pi * pow(radius, 3)

    # mass_hydrogen = pG * volume

    # print("radius is: " + str(radius) + " meters")
    # print("volume is: " + str(volume) + " cubic meters")
    # print("mass of hydrogen: " + str(mass_hydrogen) + " kilograms")

    return radius


# Returns the thrust force required from the motors to keep the backpack at a constant speed
def air_resistance(radius, cd, speed, pA):
    Area = math.pi * pow(radius, 2)
    Force_Air = (1 / 2) * pA * cd * Area * pow(speed, 2)

    # print("Thrust Force Required: " + str(Force_Air) + " Newtons")

    return Force_Air


# Returns expected battery life from an ideal motor drawing the power required to keep the backpack at a constant
# speed, capacity in amp hours
def battery_life(speed, force, battery_c, battery_voltage, idle_power):
    # idle power is power drawn from components that do not include the motors
    Power = force * speed
    Life = (battery_voltage * battery_c) / (Power + idle_power)

    # print("Battery will last for: " + str(Life) + " hours")

    return Life


def simulate(inc):
    start_time = time.time()  # begins recording simulation time
    print("simulation start")
    # range of masses for males vs balloon size
    xi = 0.1  # lower bound of masses
    xf = 30  # upper bound of masses
    i = xi
    x = []  # masses
    y = []  # balloon size
    while i <= xf:
        x.append(i)
        y.append(size_of_balloon(air_d, hydrogen_d, i))
        i += inc

    # range of operating speeds vs battery life: 10 kg, 22.2 V battery
    # 3Ah capacity
    oi = 0
    of = 1.8
    i = oi
    o = []  # operating speeds
    p = []  # battery life
    radius = size_of_balloon(air_d, hydrogen_d, 10)
    while i <= of:
        o.append(i)
        force = air_resistance(radius, cd_sphere, i, air_d)
        p.append(battery_life(i, force, 3, 22.2, idle_power_draw))
        i += inc

    # Range of masses vs battery life at the optimal operating speed determined from the last graph, 3Ah battery

    ki = 0
    kf = 40
    i = ki
    speed = 1.4  # change this, perhaps
    k = []  # masses
    b = []  # battery life
    while i <= kf:
        k.append(i)
        radius2 = size_of_balloon(air_d, hydrogen_d, i)
        force2 = air_resistance(radius2, cd_sphere, speed_walk_w, air_d)
        b.append(battery_life(speed, force2, 3, 22.2, idle_power_draw))
        i += inc

    # Range of battery capacities vs operating life at 10kg payload, and optimal speed.
    si = 0.1
    sf = 4
    i = si
    s = []  # battery capacities
    j = []  # operating life
    radius3 = size_of_balloon(air_d, hydrogen_d, 10)
    force3 = air_resistance(radius3, cd_sphere, speed_walk_w, air_d)
    while i <= sf:
        s.append(i)
        j.append(battery_life(speed, force3, i, 22.2, idle_power_draw))
        i += inc

    elapsed = time.time() - start_time  # calculates total simulation time
    print("Simulation time: " + str(elapsed) + " seconds.")

    plt.subplot(2, 2, 1)
    plt.plot(x, y, color='blue')
    plt.xlabel('mass (kg)')
    plt.ylabel('balloon radius (m)')
    plt.title('Hydrogen -> payload mass vs balloon size')

    # plt.subplot(3, 2, 2)
    # plt.plot(w, z, color='red')
    # plt.xlabel('mass (kg)')
    # plt.ylabel('balloon radius (m)')
    # plt.title('masses for females vs balloon size')

    plt.subplot(2, 2, 2)
    plt.plot(o, p, color='green')

    plt.xlabel('speed (m/s)')
    plt.ylabel('battery life (hours)')
    plt.title('Hydrogen -> operating speed vs battery life (10 kg, 22.2 V battery, 3Ah battery)')

    plt.subplot(2, 2, 3)
    plt.plot(k, b, color='orange')

    plt.xlabel('masses (kg)')
    plt.ylabel('battery life (hours)')
    plt.title('Hydrogen -> masses vs battery life (1.4 m/s, 22.2 V battery, 3Ah battery)')

    plt.subplot(2, 2, 4)
    plt.plot(s, j, color='purple')

    plt.xlabel('battery capacity (Ah)')
    plt.ylabel('battery life (hours)')
    plt.title('Hydrogen -> battery capacities vs battery life (10kg payload, 1.4 m/s, 22.2 V battery)')

    plt.tight_layout()

    plt.show()










simulate(0.001)
