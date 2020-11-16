import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import xlsxwriter


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
    for index in range(0, len(vektor)):
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


def get_leader(population, UCELOVKA):
    if UCELOVKA == 1:
        best_cost = first_dejong(population[0].position)
    if UCELOVKA == 2:
        best_cost = schweffel(population[0].position)
    if UCELOVKA == 3:
        best_cost = second_dejong(population[0].position)
    if UCELOVKA == 4:
        best_cost = rastrigin(population[0].position)
    leader = population[0]
    for individual in population:
        if UCELOVKA == 1:
            actual_cost = first_dejong(individual.position)
        if UCELOVKA == 2:
            actual_cost = schweffel(individual.position)
        if UCELOVKA == 3:
            actual_cost = second_dejong(individual.position)
        if UCELOVKA == 4:
            actual_cost = rastrigin(individual.position)
        individual.cost = actual_cost
        if actual_cost < best_cost:
            best_cost = actual_cost
            leader = individual
    return leader


# definice parametrů
# chceme pohlídat 5000*d FEZů

# 1 - first dejong
# 2 - schweffel
# 3 - second dejong
# 4 - rastrigin


def beh(dimenze, UCELOVKA):
    t = 0
    path_length = 3
    step = 0.33
    prt = 0.3
    d = dimenze  # v ukolu chce 10 a 30
    pop_size = 3 * d
    pocet_behu = 30 #TODO: POZOR, TADY MÁ BÝT 30
    pocet_accepted_fezu = 5000 * d
    data_vsech_migraci = []
    plt.figure()
    # pocet behu

    migrace = 50
    konec = 0
    counterGlobal = 0
    for _ in range(pocet_behu):
        fezcounter = 0
        # tvorba populace
        populace = []
        for i in range(pop_size):
            if UCELOVKA == 1:
                populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))
            if UCELOVKA == 2:
                populace.append(Jedinec(generate_random(d, -500, 500), 0))
            if UCELOVKA == 3:
                populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))
            if UCELOVKA == 4:
                populace.append(Jedinec(generate_random(d, -5.12, 5.12), 0))

        leader = get_leader(populace, UCELOVKA)
        fezcounter += pop_size
        # pro graf
        best_results_migrace = []
        # migrace
        counterGlobal = 0
        for _ in range(migrace):
            # ohodnot vsechny jedince v aktualni populaci (pozdeji ve foru) a ziskej leadera

            # leader je vzdy best dané migrace
            leader_of_population = leader
            # posouvej ostatni k leaderovi pomocí Step
            for jedinec in populace:
                counterGlobal += 1
                best_results_migrace.append(leader.cost)
                if konec == 1:
                    continue

                if jedinec != leader:
                    potencial_position = jedinec.position.copy()
                    # aktualizuj pozice
                    # Od sve pozice udelam 6x hups “nejak” smerem k leaderovi, zjistim kde to bylo nejlepsi s tam se vratim
                    t = 0
                    actual_cost = jedinec.cost
                    while t < path_length:
                        # PRT vektor bude vždy nový před každým skokem
                        PRTVector = generate_random(d, 0, 1)
                        #  - porovnej obsah vektoru s parametrem PRT
                        for index, cislo in enumerate(PRTVector):
                            # - jestliže je nějaké vygenerované číslo větší než PRT, pak je toto čislo sraženo na 0, jinak na 1
                            if cislo > prt:
                                PRTVector[index] = 0
                            else:
                                PRTVector[index] = 1
                        potencial_position = np.add(potencial_position,
                                                    np.subtract(leader.position, potencial_position) * t * PRTVector)
                        # zkontroluj jestli je vektor v dimenzích!
                        for index, sample in enumerate(potencial_position):
                            if UCELOVKA == 1:
                                if not -5.12 < sample < 5.12:
                                    potencial_position[index] = np.random.uniform(-5.12, 5.12)
                            if UCELOVKA == 2:
                                if not -500 < sample < 500:
                                    potencial_position[index] = np.random.uniform(-500, 500)
                            if UCELOVKA == 3:
                                if not -5.12 < sample < 5.12:
                                    potencial_position[index] = np.random.uniform(-5.12, 5.12)
                            if UCELOVKA == 4:
                                if not -5.12 < sample < 5.12:
                                    potencial_position[index] = np.random.uniform(-5.12, 5.12)
                        # zjisti zda se vylepsil
                        if UCELOVKA == 1:
                            potencial_cost = first_dejong(potencial_position)
                        if UCELOVKA == 2:
                            potencial_cost = schweffel(potencial_position)
                        if UCELOVKA == 3:
                            potencial_cost = second_dejong(potencial_position)
                        if UCELOVKA == 4:
                            potencial_cost = rastrigin(potencial_position)
                        fezcounter += 1
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
            # uklada se nejlepsi ohodnoceni z cele populace - to je ale leader
            leader = leader_of_population
        # ---konec migracniho kola---
        plt.subplot(211)
        # TODO, TADY SE TO MUSI LEPE NEJAK POCITAT
        print("counter global" + str(counterGlobal))
        print("best result migrace len:" + str(len(best_results_migrace)))
        plt.plot(range(0, counterGlobal), best_results_migrace)
        plt.title('Vsechny behy' + 'D=' + str(dimenze) + ' ucelovka' + str(UCELOVKA))
        # print(len(best_results_migrace))  # data posledniho behu, 50x
        data_vsech_migraci.append(best_results_migrace)
    # ---konec jednoho behu---


    # pole polí - jeden prvek = data jednoho běhu
    # print(data_vsech)

    pole_nejlepsich = []
    sectene_pole = [0] * counterGlobal
    # print("sectene pole:" + str(len(sectene_pole)))
    for data_migrace in data_vsech_migraci:
        # print("migrace: " + str(len(data_migrace)))
        sectene_pole = np.array(sectene_pole) + np.array(data_migrace)
        pole_nejlepsich.append(data_migrace[-1])

    sectene_pole = sectene_pole / pocet_behu
    plt.subplot(212)
    plt.plot(range(counterGlobal), sectene_pole)
    plt.title('prumery')
    plt.show(block=False)

    return pole_nejlepsich

def printHeader(worksheet, dimenze, sloupec, radek):

    worksheet.write(sloupec + str(radek), 'DIM'+str(dimenze))
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), 'MIN')
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), 'MAX')
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), 'MEAN')
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), 'MEDIAN')
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), 'STR DEV')

def printRadek(worksheet, pole_nejlepsich, nazev ,sloupec, radek):

    worksheet.write(sloupec + str(radek), nazev)
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), np.min(pole_nejlepsich))
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), np.max(pole_nejlepsich))
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), np.mean(pole_nejlepsich))
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), np.median(pole_nejlepsich))
    sloupec = chr(ord(sloupec) + 1)
    worksheet.write(sloupec + str(radek), np.std(pole_nejlepsich))


dimenze_pole = [10,30]
ucelova_funkce_pole = [1,2,3,4]

ucelovky = [
    'First dejong',
    'Schweffel',
    'Second dejong',
    'Rastrigin'
]

radek = 2
prvni_sloupec = 'C'

workbook = xlsxwriter.Workbook('EXCEL.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('C:H', 20)

for dimenze in dimenze_pole:
    printHeader(worksheet, dimenze, prvni_sloupec, radek)
    radek += 1
    for ucelova_funkce in ucelova_funkce_pole:

        pole_nejlepsich = beh(dimenze, ucelova_funkce)

        printRadek(worksheet, pole_nejlepsich, ucelovky[ucelova_funkce-1], prvni_sloupec, radek)
        radek += 1

    radek += 1


workbook.close()

#konec funkce

# 1 - first dejong
# 2 - schweffel
# 3 - second dejong
# 4 - rastrigin

# beh(10, 1)
#beh(10, 1)
# beh(10, 3)
# beh(10, 4)
#
# beh(30, 1)
# beh(3, 2)
# beh(30, 3)
# beh(30, 4)

# fig = go.Figure(data=[go.Table(header=dict(values=['Median', 'Max', 'Min', 'Mean', 'STADEV']),
#                  cells=dict(values=[[np.median(pole_nejlepsich)], [np.max(pole_nejlepsich)],[np.min(pole_nejlepsich)],[np.mean(pole_nejlepsich)],[np.std(pole_nejlepsich)]]))
#                      ])
# fig.show()

plt.show()

