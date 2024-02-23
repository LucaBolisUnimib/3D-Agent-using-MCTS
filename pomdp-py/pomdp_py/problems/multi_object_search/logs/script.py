import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from ast import literal_eval as make_tuple
f = open("log.txt", "r")
dati = dict()
count = dict()
for x in f:
    (step, depth, time) = make_tuple(x)
    if (depth, time) not in dati:
        dati[(depth, time)] = float(step)
        count[(depth, time)] = 1
    else:
        dati[(depth, time)] += float(step)
        count[(depth, time)] += 1
for x in dati:
    dati[x] = dati[x] / count[x]

colors = {}
defaultVal = [(40, "#007a21"), (55, "#5cff4d"), (70, "#d4f035"), (85, "#ffff00"), (100, "#ffa500"),(1000, "#ff0000")]

for x in np.arange(0, 500, .5):
    place = False
    for val, col in defaultVal:
        if not place and x <= val:
            colors[x] = col
            place = True

x = np.empty(0)
y = np.empty(0)
val = np.empty(0)

for dat in dati:
    x = np.append(x, dat[0])
    y = np.append(y, dat[1])
    val = np.append(val, dati[dat])

fig, ax = plt.subplots(1, 1)
scatter = ax.scatter(x, y, c=[colors[n] for n in val], alpha=0.5)
prec = 0
for value, color in defaultVal:
    plt.scatter(x, y, c=[colors[n] for n in val], alpha=0.5, label=str(prec) + " < X ≤ " + str(value))
    prec = value

ax.set_xlabel("Max depth")
ax.set_ylabel("Planning time")

plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='Azioni', loc = [1, 0])

plt.show()