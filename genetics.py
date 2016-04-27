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
        
def three_parent_tournament(p1, p2, p3, f1, f2, f3) :
    if f1 >= f2 or f1 >= f3:
        if f2 >= f3 :
            return p1, p2
        else :
            return p1, p3
    elif f2 >= f3 :
        if f1 >= f3 :
            return p1, p2
        else :
            return p2, p3
    else :
        if f1 >= f2 :
            return p1, p3
        else :
            return p2, p3
