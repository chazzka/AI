import numpy as np
import matplotlib.pyplot as plt

"""
PSO
částice - jedno řešení
        - pozice: xi (vektor)
            xi(t) = xi(t-1) + vi(t)     (17)
        - rychlost: vi
            vi(t) = vi(t-1) + c1*rand1*(pi-xi(t-1)) + c2*rand2*(pg-xi(t-1))     (18)
        kde
        c1,c2 - kladná čísla c1+c2 < 4
        rand1, rand2 - random 0-1
"""

"""
1 - first dejong
2 - schweffel
"""
DEFINE_TEST_FUNCTION = 1


class Particle:
    def __init__(self, x):
        self.x = x
        self.v = 0
        self.pBest = 1000000000


# inicializuj učelovou funkci
def first_dejong(vector):
    fjd_result = 0
    for sample in vector:
        fjd_result += pow(sample, 2)
    return fjd_result


def schweffel(vector):
    s_result = 0
    for sample in vector:
        s_result += - sample * np.sin(np.sqrt(np.abs(sample)))
    return s_result


def random_position(minimum, maximum, dimension):
    """
    first_dejong -5.12 to 5.12
    schweffel -500 to 500
    """
    vector = []
    for sample in range(0, dimension):
        vector.append(np.random.uniform(minimum, maximum))
    return vector


databehu = []
runs = 0
while runs < 30:
    # inicilizuj promenne pro globalni rovnici
    pi = []
    gbest = 10000
    pg = []
    c1 = 2
    c2 = 2
    w = 0.7298

    # inicializuj hejno částic
    # každé částici přiřaď náhodnou pozici
    swarm = []
    number_of_particles = 50
    for i in range(0, number_of_particles):
        if DEFINE_TEST_FUNCTION == 1:
            particle = Particle(random_position(-5.12, 5.12, 10))
            swarm.append(particle)
        if DEFINE_TEST_FUNCTION == 2:
            particle = Particle(random_position(-500, 500, 5))
            swarm.append(particle)

    results = []
    iterations = []
    # DO
    particle_iterator = 0
    swarm_iterator = 0
    while swarm_iterator < 1600:
        for particle in swarm:
            # každé částici vypočítej hodnotu její fitness (účelové) funkce
            if DEFINE_TEST_FUNCTION == 1:
                actual_fitness = first_dejong(particle.x)
            if DEFINE_TEST_FUNCTION == 2:
                actual_fitness = schweffel(particle.x)
            # tuto hodnotu porovnej s jeji pbest, pokud je lepší, do pi ulož současnou polohu, jinak nic
            if actual_fitness < particle.pBest:
                particle.pBest = actual_fitness
                pi = particle.x
            # najdi částici s nejlepší fitness, tato hodnota je gbest a poloha této částice je pg
            if actual_fitness < gbest:
                gbest = actual_fitness
                pg = particle.x
            # aktualizuj pozice a rychlosti částic dle rovnic popsaných výše (17) a (18)
            particle.v = w * particle.v + np.dot(c1 * np.random.uniform(0, 1), (np.subtract(pi, particle.x))) + np.dot(
                c2 * np.random.uniform(0, 1), (np.subtract(pg, particle.x)))
            particle.x = np.add(particle.x, particle.v)
            # zkontroluj jestli je vektor v dimenzích!
            for index, sample in enumerate(particle.x):
                if DEFINE_TEST_FUNCTION == 1:
                    if not -5.12 < sample < 5.12:
                        particle.x[index] = np.random.uniform(-5.12, 5.12)
                if DEFINE_TEST_FUNCTION == 2:
                    if not -500 < sample < 500:
                        particle.x[index] = np.random.uniform(-500, 500)

            # uloz si gbest kazdeho jedince v hejnu, kazdy dalsi by ho mel mit lepsi
            results.append(gbest)
            particle_iterator += 1
            iterations.append(particle_iterator)
        swarm_iterator += 1
    databehu.append(results)
    # graf vsech behu
    #plt.plot(iterations, results)
    runs += 1

prumerybehu = []

arr_transpose = np.array(databehu).transpose()
for item in arr_transpose:
    prumerybehu.append(np.average(item))

# graf prumeru
plt.plot(range(0, len(prumerybehu)), prumerybehu)
plt.show()
