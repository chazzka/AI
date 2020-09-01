import numpy as np
import matplotlib.pyplot as plt

"""
SOMA
     - Specimen - exemplář - pole o 10 dimenzích?
     - PathLength - jak daleko se zastaví aktivní jedinec od vedoucího
     - Step - velikost skoku
     - PRT - pertubace - stochastická složka
     - D - dimenze ? souvisí se Specimen?
     - PopSize - počet jedinců v populaci - 10xD
     - Migrace - "Generace"
     - (AcceptedError) - velikost chyby (optional)
"""

# 1 - first dejong
# 2 - schweffel
DEFINE_UCELOVA_FUNKCE = 2

class Jedinec:
    def __init__(self, position):
        self.position = position


# definice účelové funkce
def first_dejong(vektor):
    fdj_result = 0
    for i, _ in enumerate(vektor):
        fdj_result += pow(vektor[i], 2)
    return fdj_result


def schweffel(vektor):
    result = 0
    for index, _ in enumerate(vektor):
        result += - vektor[index] * np.sin(np.sqrt(np.abs(vektor[index])))
    return result


# pomocné funkce
def generate_random(size, minimum, maximum):
    vector = []
    for i in range(size):
        vector.append(np.random.uniform(minimum, maximum))
    return vector


def get_leader(population):
    if DEFINE_UCELOVA_FUNKCE == 1:
        best_cost = first_dejong(population[0].position)
    if DEFINE_UCELOVA_FUNKCE == 2:
        best_cost = schweffel(population[0].position)
    leader = population[0]
    for individual in population:
        if DEFINE_UCELOVA_FUNKCE == 1:
            actual_cost = first_dejong(individual.position)
        if DEFINE_UCELOVA_FUNKCE == 2:
            actual_cost = schweffel(individual.position)
        if actual_cost < best_cost:
            best_cost = actual_cost
            leader = individual
    return leader


# definice parametrů
t = 0
path_length = 3
step = 0.11
prt = 0.1
d = 10
pop_size = 3 * d
migrace = 50

# pocet behu
for _ in range(10):

    # tvorba populace
    populace = []
    for i in range(pop_size):
        if DEFINE_UCELOVA_FUNKCE == 1:
            populace.append(Jedinec(generate_random(d, -5.12, 5.12)))
        if DEFINE_UCELOVA_FUNKCE == 2:
            populace.append(Jedinec(generate_random(d, -500, 500)))

    # pro graf
    best_results = []
    # migrace
    for _ in range(migrace):
        # ohodnot vsechny jedince v aktualni populaci (pozdeji ve foru) a ziskej leadera
        # uklada se nejlepsi ohodnoceni z cele populace - to je ale leader
        leader = get_leader(populace)

        # leader je vzdy best dané migrace
        # if DEFINE_UCELOVA_FUNKCE == 1:
        #     best_results.append(first_dejong(leader.position))
        # if DEFINE_UCELOVA_FUNKCE == 2:
        #     best_results.append(schweffel(leader.position))

        # posouvej ostatni k leaderovi pomocí Step
        for jedinec in populace:
            # než začne jedinec svou cestu, je vygenerovan nahodny vektor
            PRTVector = generate_random(d, 0, 1)
            #  - porovnej obsah vektoru s parametrem PRT
            for index, cislo in enumerate(PRTVector):
                # - jestliže je nějaké vygenerované číslo větší než PRT, pak je toto čislo sraženo na 0, jinak na 1
                if cislo > prt:
                    PRTVector[index] = 0
                else:
                    PRTVector[index] = 1
            # ohodnot jeho soucasnou pozici
            if DEFINE_UCELOVA_FUNKCE == 1:
                actual_cost = first_dejong(jedinec.position)
            if DEFINE_UCELOVA_FUNKCE == 2:
                actual_cost = schweffel(jedinec.position)
            if jedinec != leader:
                potencial_position = jedinec.position.copy()
                # aktualizuj pozice
                # Od sve pozice udelam 6x hups “nejak” smerem k leaderovi, zjistim kde to bylo nejlepsi s tam se vratim
                t = 0
                best_cost = actual_cost
                best_position = potencial_position
                while t < path_length:
                    potencial_position = np.add(potencial_position,
                                                np.subtract(leader.position, potencial_position) * t * PRTVector)
                    # zkontroluj jestli je vektor v dimenzích!
                    for index, sample in enumerate(potencial_position):
                        if DEFINE_UCELOVA_FUNKCE == 1:
                            if not -5.12 < sample < 5.12:
                                potencial_position[index] = np.random.uniform(-5.12, 5.12)
                        if DEFINE_UCELOVA_FUNKCE == 2:
                            if not -500 < sample < 500:
                                potencial_position[index] = np.random.uniform(-500, 500)
                    # aktualizuj
                    if DEFINE_UCELOVA_FUNKCE == 1:
                        potencial_cost = first_dejong(potencial_position)
                    if DEFINE_UCELOVA_FUNKCE == 2:
                        potencial_cost = schweffel(potencial_position)
                    if potencial_cost < best_cost:
                        best_cost = potencial_cost
                        best_position = potencial_position
                    t += step
                # po dokončení whilu se vrátím tam kde to bylo nejlepsi
                jedinec.position = best_position
        print(best_cost)
        best_results.append(best_cost)
    # ---konec migracniho kola---
    # print(best_results)
    # print("a")
    plt.plot(range(len(best_results)), best_results)
plt.show()
