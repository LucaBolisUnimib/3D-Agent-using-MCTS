import numpy as np

sorted = False

dispositions = [[(3, 8), (5, 1), (4, 5)],
                [(7, 6), (0, 1), (4, 5)],
                [(0, 6), (5, 6), (9, 8)],
                [(8, 0), (4, 3), (6, 7)]]
probabilty =    [0.5, 0.3, 0.1, 0.1]
default_grid =  "r.........\n" + \
                "....x.....\n" + \
                "......xx..\n" + \
                ".x........\n" + \
                ".xx......x\n" + \
                "..........\n" + \
                ".....x...x\n" + \
                "....xx...x\n" + \
                "..........\n" + \
                "x...xx...x"
length = default_grid.count("\n") + 1
width = (len(default_grid) - length + 1) // 10
dispositionid = np.random.choice(list(range(len(dispositions))), 1, p = probabilty)[0]
dispositionid = 0
"""
First disposition (0.5 probability):
r.........
....x.....
......xx..
.x......T.
.xx..T...x
.T........
.....x...x
....xx...x
..........
x...xx...x

Second disposition (0.3 probability):
rT........
....x.....
......xx..
.x........
.xx...T..x
..........
.....x...x
....xxT..x
..........
x...xx...x

Third disposition (0.1 probability):
r.....T...
....x.....
......xx..
.x........
.xx......x
......T...
.....x...x
....xx...x
..........
x...xx..Tx

Fourth disposition (0.1 probability):
r.........
....x.....
......xx..
.x........
.xxT.....x
..........
.....x.T.x
....xx...x
T.........
x...xx...x
"""