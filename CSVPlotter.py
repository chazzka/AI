import csv
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

import os, glob
from tkinter import Tk
from tkinter.filedialog import askdirectory
from pathlib import Path

mediany = []
maxy = []
miny = []
meany = []
deviace = []
nazvy_funkci = []

polePrumeruVsechFilu = []
poleIndexuGlobal = []


Tk().withdraw()
openPath = askdirectory(title='Select folder with csv files')
savePath = askdirectory(title='Select where to save results')
folder_path = openPath
for filename in glob.glob(os.path.join(folder_path, '*.csv')):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        poleCSV = []

        for radek in spamreader:
            poleCSV.append(radek)

    poleHodnotSloupcu = []

    polePrumeru = []
    for radek in poleCSV:
        radekPrumeru = radek.copy()
        radekPrumeru.reverse()
        radekPrumeru.pop()
        tempRadek = np.array(radekPrumeru)
        ciselnyTempRadek = tempRadek.astype(np.float)
        # print(ciselnyTempRadek)
        polePrumeru.append(sum(ciselnyTempRadek) / len(ciselnyTempRadek))

    polePrumeruVsechFilu.append(polePrumeru)

    for i in range(0, 31):
        poleSloupce = []
        for radek in poleCSV:
            ciselnaHodnota = float(radek[i])
            poleSloupce.append(ciselnaHodnota)
        poleHodnotSloupcu.append(poleSloupce)

    name_of_file = filename.split('\\')[1].split('.')[0]
    poleIndexu = poleHodnotSloupcu.pop(0)
    poleIndexuGlobal = poleIndexu.copy()
    poleVysledku = []

    Path(savePath + "/imgresults").mkdir(parents=True, exist_ok=True)
    plt.figure()
    for i in poleHodnotSloupcu:
        plt.plot(poleIndexu, i)
        plt.yscale('log')
        plt.title(name_of_file)
        plt.savefig(savePath + '/imgresults/' + name_of_file)
        poleVysledku.append(i)
    plt.close()

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

    Path(savePath + "/imgresults/prumery").mkdir(parents=True, exist_ok=True)
    # toto je jedno csv:
    # chceme graf 1x prumer
    plt.figure()
    plt.plot(poleIndexu, polePrumeru)
    plt.yscale('log')
    plt.title(name_of_file + 'prumer')
    plt.savefig(savePath + '/imgresults/prumery/' + name_of_file)
    plt.close()
    # chceme graf se vsemi prumery jednotlivych dimenzi v jednom

fig = go.Figure(data=[go.Table(header=dict(values=['Nazev funkce', 'Median', 'Max', 'Min', 'Mean', 'STADEV']),
                               cells=dict(values=[nazvy_funkci, mediany, maxy,
                                                  miny, meany,
                                                  deviace]))
                      ])

Path(savePath + "/statresults").mkdir(parents=True, exist_ok=True)
fig.write_html(savePath + "/statresults/statistika.html")
# fig.show()

plt.figure()
for i in polePrumeruVsechFilu:
    plt.plot(poleIndexuGlobal, i)
    plt.yscale('log')
    plt.title('prumery ' + folder_path)
    plt.legend(['BC', 'C1', 'C3', 'C2', 'H1', 'H3', 'H2', 'Lun', 'Ros', 'RotSch'])
    plt.savefig(savePath + '/imgresults/prumery/prumeryJedneDimenze')

plt.close()
