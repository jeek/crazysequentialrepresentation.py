from copy import deepcopy
from pickle import loads, dumps
from math import log

upperlimit = 10 ** 15

for (filename, seed) in [("csrup.txt", [1, 2, 3, 4, 5, 6, 7, 8, 9]), ("csrdown.txt", [9, 8, 7, 6, 5, 4, 3, 2, 1])]:
    queue = {9: set([dumps(seed)])}

    # First, handle concatenation
    for queuelevel in xrange(9, 1, -1):
        queue[queuelevel - 1] = set()
        for i in queue[queuelevel]:
            i = loads(deepcopy(i))
            for j in xrange(len(i) - 1):
                temp = deepcopy(i)
                temp.insert(j, int(str(temp.pop(j)) + str(temp.pop(j))))
                queue[queuelevel - 1].add(dumps(temp))

    # Now, the other operators
    for i in queue[9]:
        print loads(i)
    for queuelevel in xrange(9, 1, -1):
        for i in queue[queuelevel]:
            i = loads(deepcopy(i))
            for j in xrange(len(i) - 1):
                # Addition
                temp = deepcopy(i)
                a = temp.pop(j)
                b = temp.pop(j)
                temp.insert(j, a + b)
                queue[queuelevel - 1].add(dumps(temp))
                # Multiplication
                temp = deepcopy(i)
                a = temp.pop(j)
                b = temp.pop(j)
                temp.insert(j, a * b)
                queue[queuelevel - 1].add(dumps(temp))
                # Exponentiation
                temp = deepcopy(i)
                a = temp.pop(j)
                b = temp.pop(j)
                if b * log(a) / log(10) <= log(upperlimit) / log(10) + 1:
                    temp.insert(j, a ** b)
                    queue[queuelevel - 1].add(dumps(temp))
    outputfile = open(filename, "w")
    outputfile.write("\n".join(str(j) for j in sorted(set(loads(i)[0] for i in queue[1] if loads(i)[0] <= upperlimit))))
    outputfile.close()
