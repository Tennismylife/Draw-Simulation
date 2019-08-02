## run simulations of a single-elimination tournament

import random, copy
from createTuple import createTuple ## gist: 778481
from writeMatrixCSV import writeMatrixCSV ## gist: 778484

def calcWp(x, y, e):
    x = float(x)
    y = float(y)
    return (x**e)/((x**e)+(y**e))

def findRoundWinners(roundPlayers):
    ## get each pair of players, return list of 'winners'
    nextRound = []
    roundMatches = len(roundPlayers)/2
    for i in range(int(roundMatches)):
        j = i*2
        playerOne = roundPlayers[j]
        playerTwo = roundPlayers[j+1]
        oneWp = calcWp(pointDict[playerOne], pointDict[playerTwo], e)
        if random.random() < oneWp: winner = playerOne
        else:   winner = playerTwo
        nextRound.append(winner)
    return nextRound

e = 1.1
sims = 300000
draw = createTuple('aussie_draw_2011.csv')

blankResults = {1: 0,
                2: 0,
                4: 0,
                8: 0
                }

for z in [17, 33, 65]:
    if len(draw) > z:
        dsize = (z-1)
        blankResults[dsize] = 0

pointDict = {}
firstRound = []
resultDict = {}
for pl in draw:
    pointDict[pl[0]] = int(pl[2])
    firstRound.append(pl[0])
    resultDict[pl[0]] = copy.deepcopy(blankResults)

## run the simulation
for x in range(sims):
    if x % (sims/10) == 0:    print (x)
    nextRound = firstRound
    while True:
        nextRound = findRoundWinners(nextRound)
        n = len(nextRound)
        for p in nextRound:
            resultDict[p][n] += 1
        if n == 1:  break

rds = []
for z in [65, 33, 17]:
    if len(draw) > z:
        rdname = 'R' + str(z-1)
        rds.append(rdname)

header = ['Player', '', 'points'] + rds + ['QF', 'SF', 'F', 'W']

resultTable = [header]
for pl in draw:
    p = pl[0]
    row = pl[:3]
    for result in [8, 4, 2, 1]:
        perc = resultDict[p][result]/float(sims)
        row.append(perc)
    resultTable.append(row)

writeMatrixCSV(resultTable, 'aussie_sim_results_2011.csv')
