from copy import deepcopy as copy
from pickle import loads,dumps
from math import log10

upperlimit = 1000000

for (outputfilename, queue) in [("csrup.txt", [dumps(range(1,4))]), ("csrdown.txt", [dumps(range(3,0,-1))])]:
#for (outputfilename, queue) in [("csrup.txt", [dumps(range(1,10))]), ("csrdown.txt", [dumps(range(9,0,-1))])]:

    path = {}
    i = 0
    heh = 0
    while i < len(queue):
        current = loads(queue[i])
        path[dumps(current)] = dumps(current)
        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, int(str(temp.pop(j)) + str(temp.pop(j))))
            if dumps(temp) not in queue:
                queue.append(dumps(temp))
        i += 1

    i = len(queue)
    while i > 0:
        i -= 1
        current = loads(queue[i])
        current[0] *= -1
        path[dumps(current)] = dumps(current)
        queue.append(dumps(current))

    alreadydone = set()
    rofl = 0
    while len(queue):

        current = loads(queue.pop())
        heh = len(queue)
        alreadydone.add(dumps(current))

        for j in range(len(current) - 1):
            temp = copy(current)
            if temp[j] > 0 and temp[j + 1] > 0 and temp[j + 1] * log10(temp[j]) <= log10(upperlimit):
                temp.insert(j, temp.pop(j) ** temp.pop(j))
                path[dumps(temp)] = path[dumps(current)]
                if dumps(temp) not in alreadydone:
                    queue.append(dumps(temp))

                path[dumps(temp)] = path[dumps(current)]
                temp2 = loads(path[dumps(temp)])
                temp2.insert(j, "(" + str(temp2.pop(j)) + " ** " + str(temp2.pop(j)) + ")")
                path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            if temp[j + 1] != 0 and temp[j] % temp[j + 1] == 0:
                temp.insert(j, temp.pop(j) / -temp.pop(j))
                path[dumps(temp)] = path[dumps(current)]
                if dumps(temp) not in alreadydone:
                    queue.append(dumps(temp))

                path[dumps(temp)] = path[dumps(current)]
                temp2 = loads(path[dumps(temp)])
                temp2.insert(j, "(" + str(temp2.pop(j)) + " / -" + str(temp2.pop(j)) + ")")
                path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            if temp[j + 1] != 0 and temp[j] % temp[j + 1] == 0:
                temp.insert(j, temp.pop(j) / temp.pop(j))
                path[dumps(temp)] = path[dumps(current)]
                if dumps(temp) not in alreadydone:
                   queue.append(dumps(temp))

                path[dumps(temp)] = path[dumps(current)]
                temp2 = loads(path[dumps(temp)])
                temp2.insert(j, "(" + str(temp2.pop(j)) + " / " + str(temp2.pop(j)) + ")")
                path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) * -temp.pop(j))
            path[dumps(temp)] = path[dumps(current)]
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))

            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " * -" + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) * temp.pop(j))
            path[dumps(temp)] = path[dumps(current)]
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))

            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " * " + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) - -temp.pop(j))
            path[dumps(temp)] = path[dumps(current)]
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))

            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " - -" + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) + -temp.pop(j))
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))
            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " + -" + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) - temp.pop(j))
            path[dumps(temp)] = path[dumps(current)]
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))

            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " - " + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, temp.pop(j) + temp.pop(j))
            if dumps(temp) not in alreadydone:
                queue.append(dumps(temp))

            path[dumps(temp)] = path[dumps(current)]
            temp2 = loads(path[dumps(temp)])
            temp2.insert(j, "(" + str(temp2.pop(j)) + " + " + str(temp2.pop(j)) + ")")
            path[dumps(temp)] = dumps(temp2)

    outputfile = open(outputfilename, "w")
    for i in path.keys():
        if len(loads(i)) == 1 and abs(loads(i)[0] <= 1000000000):
            outputfile.write(str(loads(i)[0]) + ": " + str(loads(path[i])[0]) + "\n")
