import random

def randomParents(chances) :
    choiceOne = random.random()
    parentOne = -1
    for x in range(0, len(chances)) :
        if(chances[x] >= choiceOne) :
            parentOne = x
            break
    parentTwo = -1
    while parentTwo == -1 or parentTwo == parentOne :
        choiceTwo = random.random()
        for x in range(0, len(chances)) :
            if(chances[x] >= choiceTwo) :
                parentTwo = x
                break
    return parentOne, parentTwo

def n_parent_tournament(ps, fs) :
    top = ps[0]
    topVal = fs[0]
    topTwo = ps[1]
    topTwoVal = fs[1]
    if top < topTwo :
        topVal = fs[1]
        top = ps[1]
        topTwo = ps[0]
        topTwoVal = fs[0]
    for x in range(2, len(ps)) :
        if fs[x] > topTwoVal :
            topTwo = ps[x]
            topTwoVal = fs[x]
            if topTwoVal > topVal :
                tmp = top
                tmpVal = topVal
                top = topTwo
                topVal = topTwoVal
                topTwo = tmp
                topTwoVal = tmpVal
    return top, topTwo
        
#realized I didn't need this but didn't feel like fixing stuff that may have used it
def three_parent_tournament(p1, p2, p3, f1, f2, f3) :
    return n_parent_tournament([p1, p2, p3], [f1, f2, f3])

#find worst member in a set
def n_worst_creature(ps, fs) :
    worst = ps[0]
    worstVal = fs[0]
    for x in range(1, len(ps)) :
        if(fs[x] < worstVal) :
            worstVal = fs[x]
            worst = ps[x]
    return worst

def breed_floats(f1, f2, mrate, rand = random) :
    rfs = []
    for x in range(0, len(f1)) :
        if(rand.random() < mrate) :
            rfs.append(rand.random() * 2 - 1)
        else :
            if rand.random() < 0.5 :
                rfs.append(f1[x])
            else :
                rfs.append(f2[x])
    return rfs