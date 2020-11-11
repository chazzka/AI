import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
# 3 - second dejong
# 4 - rastrigin
DEFINE_UCELOVA_FUNKCE = 3


class Jedinec:
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost


# minumum v 0
def rastrigin(candidates):
    fitness = []
    fit = 10 * len(candidates) + sum([(x ** 2 - 10 * np.cos(2 * np.pi * x)) for x in candidates])
    fitness.append(fit)
    return fitness


# definice účelové funkce
# minimum je v 0
def first_dejong(vektor):
    fdj_result = 0
    for i, _ in enumerate(vektor):
        fdj_result += pow(vektor[i], 2)
    return fdj_result


# minimum je v 420.9687*D
def schweffel(vektor):
    result = 0
    for index, _ in enumerate(vektor):
        result += - vektor[index] * np.sin(np.sqrt(np.abs(vektor[index])))
    return result


def second_dejong(vektor):
    sjd_result = 0
    for i in range(0, len(vektor)):
        sjd_result += 100 * (vektor[i] - 1) ** 2 + (1 - vektor[i]) ** 2
    return sjd_result


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
    if DEFINE_UCELOVA_FUNKCE == 3:
        best_cost = second_dejong(population[0].position)
    if DEFINE_UCELOVA_FUNKCE == 4:
        best_cost = rastrigin(population[0].position)
    leader = population[0]
    for individual in population:
        if DEFINE_UCELOVA_FUNKCE == 1:
            actual_cost = first_dejong(individual.position)
        if DEFINE_UCELOVA_FUNKCE == 2:
            actual_cost = schweffel(individual.position)
        if DEFINE_UCELOVA_FUNKCE == 3:
            actual_cost = second_dejong(individual.position)
        if DEFINE_UCELOVA_FUNKCE == 4:
            actual_cost = rastrigin(individual.position)
        individual.cost = actual_cost
        if actual_cost < best_cost:
            best_cost = actual_cost
            leader = individual
    return leader


# definice parametrů
# chceme pohlídat 5000*d FEZů

t = 0
path_length = 3
step = 0.33
prt = 0.3
d = 10  # v ukolu chce 10 a 30
pop_size = 3 * d
migrace = 50
pocet_behu = 30
pocet_accepted_fezu = 5000 * d

data_vsech_migraci = []
plt.figure()
# pocet behu

konec = 0
for _ in range(pocet_behu):
    fezcounter = 0
    # tvorba populace
    populace = []
    for i in range(pop_size):
        if DEFINE_UCELOVA_FUNKCE == 1:
            populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))
        if DEFINE_UCELOVA_FUNKCE == 2:
            populace.append(Jedinec(generate_random(d, -500, 500), 0))
        if DEFINE_UCELOVA_FUNKCE == 3:
            populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))
        if DEFINE_UCELOVA_FUNKCE == 4:
            populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))

    leader = get_leader(populace)
    fezcounter += pop_size
    # pro graf
    best_results_migrace = []
    # migrace
    for _ in range(migrace):
        # ohodnot vsechny jedince v aktualni populaci (pozdeji ve foru) a ziskej leadera
        # uklada se nejlepsi ohodnoceni z cele populace - to je ale leader

        # leader je vzdy best dané migrace
        best_results_migrace.append(leader.cost)

        leader_of_population = leader
        # posouvej ostatni k leaderovi pomocí Step
        for jedinec in populace:
            if konec == 1:
                continue
            # než začne jedinec svou cestu, je vygenerovan nahodny vektor
            PRTVector = generate_random(d, 0, 1)
            #  - porovnej obsah vektoru s parametrem PRT
            for index, cislo in enumerate(PRTVector):
                # - jestliže je nějaké vygenerované číslo větší než PRT, pak je toto čislo sraženo na 0, jinak na 1
                if cislo > prt:
                    PRTVector[index] = 0
                else:
                    PRTVector[index] = 1

            if jedinec != leader:
                potencial_position = jedinec.position.copy()
                # aktualizuj pozice
                # Od sve pozice udelam 6x hups “nejak” smerem k leaderovi, zjistim kde to bylo nejlepsi s tam se vratim
                t = 0
                actual_cost = jedinec.cost
                actual_position = potencial_position
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
                        if DEFINE_UCELOVA_FUNKCE == 3:
                            if not -5.12 < sample < 5.12:
                                potencial_position[index] = np.random.uniform(-5.12, 5.12)
                        if DEFINE_UCELOVA_FUNKCE == 2:
                            if not -5.12 < sample < 5.12:
                                potencial_position[index] = np.random.uniform(-5.12, 5.12)
                    # zjisti zda se vylepsil
                    if DEFINE_UCELOVA_FUNKCE == 1:
                        potencial_cost = first_dejong(potencial_position)
                    if DEFINE_UCELOVA_FUNKCE == 2:
                        potencial_cost = schweffel(potencial_position)
                    if DEFINE_UCELOVA_FUNKCE == 3:
                        potencial_cost = second_dejong(potencial_position)
                    if DEFINE_UCELOVA_FUNKCE == 4:
                        potencial_cost = rastrigin(potencial_position)
                    fezcounter += 1
                    #print("fez counter je:")
                    #print(fezcounter)
                    if fezcounter > pocet_accepted_fezu:
                        #print("fez counter je vesti, koncim")
                        konec = 1
                        break
                    # pokud ano, aktualizuj
                    if potencial_cost < actual_cost:
                        if potencial_cost < leader.cost:
                            leader_of_population.position = potencial_position
                            leader_of_population.cost = potencial_cost
                        jedinec.cost = potencial_cost
                        jedinec.position = potencial_position
                    t += step
                # ----- konec whilu populace -----
        leader = leader_of_population
    # ---konec migracniho kola---
    plt.subplot(211)
    plt.plot(range(len(best_results_migrace)), best_results_migrace)
    plt.title('Vsechny behy')

    # print(len(best_results_migrace))  # data posledniho behu, 50x
    data_vsech_migraci.append(best_results_migrace)
# ---konec jednoho behu---


# pole polí - jeden prvek = data jednoho běhu
# print(data_vsech)

pole_nejlepsich = []
sectene_pole = [0] * migrace
for migrace in data_vsech_migraci:
    sectene_pole = np.array(sectene_pole) + np.array(migrace)
    pole_nejlepsich.append(migrace[-1])

print(np.sort(pole_nejlepsich))

print(np.median(pole_nejlepsich))
print(np.max(pole_nejlepsich))
print(np.min(pole_nejlepsich))
print(np.mean(pole_nejlepsich))
print(np.std(pole_nejlepsich))


fig = go.Figure(data=[go.Table(header=dict(values=['Median', 'Max', 'Min', 'Mean', 'STADEV']),
                 cells=dict(values=[[np.median(pole_nejlepsich)], [np.max(pole_nejlepsich)],[np.min(pole_nejlepsich)],[np.mean(pole_nejlepsich)],[np.std(pole_nejlepsich)]]))
                     ])
fig.show()


sectene_pole = sectene_pole / pocet_behu
print(sectene_pole)
plt.subplot(212)
plt.plot(range(len(sectene_pole)), sectene_pole)
plt.title('prumery')
plt.show()

# TODO: statisticka tabulka a pohlidat fezy
