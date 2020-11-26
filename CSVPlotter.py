import csv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

import os, glob

mediany = []
maxy = []
miny = []
meany = []
deviace = []
nazvy_funkci = []

folder_path = 'csvresults10'
for filename in glob.glob(os.path.join(folder_path, '*.csv')):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        plt.figure()
        poleCSV = []

        for radek in spamreader:
            poleCSV.append(radek)

    poleHodnotSloupcu = []

    for i in range(0, 31):
        poleSloupce = []
        for radek in poleCSV:
            ciselnaHodnota = float(radek[i])
            poleSloupce.append(ciselnaHodnota)
        poleHodnotSloupcu.append(poleSloupce)

    name_of_file = filename.split('\\')[1].split('.')[0]
    test = poleHodnotSloupcu.pop(0)
    # print(len(test))
    # print(poleHodnot[1])
    poleVysledku = []

    for i in poleHodnotSloupcu:
        plt.plot(test, i)
        plt.title(name_of_file)
        plt.savefig('imgresults/' + name_of_file)
        poleVysledku.append(i)

    lastResults = []
    # je jich 30
    for run in poleHodnotSloupcu:
        lastResults.append(run[len(run) - 1])

    mediany.append(np.median(lastResults))
    maxy.append(np.max(lastResults))
    miny.append(np.min(lastResults))
    meany.append(np.mean(lastResults))
    deviace.append(np.std(lastResults))
    nazvy_funkci.append(name_of_file)

fig = go.Figure(data=[go.Table(header=dict(values=['Nazev funkce', 'Median', 'Max', 'Min', 'Mean', 'STADEV']),
                               cells=dict(values=[nazvy_funkci, mediany, maxy,
                                                  miny, meany,
                                                  deviace]))
                      ])
fig.write_html("statresults/statistika.html")
# fig.show()
