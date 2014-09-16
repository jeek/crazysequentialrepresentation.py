#!/usr/bin/env python

upperlimit = 10000000
maxcrazy = 9

from math import log10 as log
import signal
import heapq
import shelve
answers = shelve.open("answers.txt")
from gmpy import is_square
from copy import deepcopy as copy
from pickle import loads, dumps
from fractions import Fraction
factorials = [1]
while len(factorials) < 30:
    factorials.append(factorials[-1] * len(factorials))
print factorials

def donothingandlikeit(argument, otherargument = ""):
    pass

def jabs(n):
    if n >= 0:
        return n
    return n * n

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def score(entry):
    enter = "".join([str(i) for i in entry])
#    if len(entry) == 1:
#        return 1
    result = 100000000000 * len(entry)
    result += 10 * enter.count("+")
    result += 100 * enter.count("*")
    result += 10000 * enter.count("^")
    result += 100 * enter.count("-")
    result += 1000000 * enter.count("/")
    result += 100000000 * enter.count("s")
    result += 10000000 * enter.count("!")
    return result
#    print entry, answers
#     print entry, sum([abs(i[0]) + abs(i[1]) for i in entry])
    return len("".join([str(i) for i in entry]))
queues = []
for i in range(1, maxcrazy + 1):
    for j in range(i + 1, maxcrazy + 1):
        queues.append(([range(i, j + 1),], "upper.txt"))
        queues.append(([range(j, i - 1, -1),], "lower.txt"))
        
def queueslensort(queueitem):
    return len(queueitem[0][0])

queues.sort(key=queueslensort)

for (queue, file) in queues:
    answers.clear()
    answers.sync()
    writefile = open(file, "a")
    i = 0
    while i < len(queue):
        current = queue[i]
        for j in range(len(current) - 1):
            temp = copy(current)
            temp.insert(j, int(str(temp.pop(j)) + str(temp.pop(j))))
            good = True
            for k in queue:
                if dumps(k) == dumps(temp):
                    good = False
            if temp not in queue:
                queue.append(temp)
        i += 1
    for i in range(maxcrazy):
        for j in copy(queue):
            try:
                j[i] *= -1
                queue.append(j)
            except:
                pass
    for i in queue:
        answers[str([(l, 1) for l in i])] = ["(" + str(k) + ")" for k in i]
    i = 0
    while i < len(queue):
        queue[i] = [(j, 1) for j in queue[i]]
        queue[i] = (len(queue[i]), queue[i])
        i += 1
#    for i in queue:
#        print i
#    print queue
    heapq.heapify(queue)
    if True:
        while len(queue) > 0:
#          queue[ii:].sort()
            (curscore, current) = heapq.heappop(queue)
#            print current
            try:
                stringrep = answers[str(current)]
            except:
                stringrep = str(current)
            if len(current) == 1:
                if current[0][1] == 1:
                    if current[0][0] >= 0 and current[0][0] <= upperlimit:
                        i = sorted([str(k) for k in str([l[0] for l in current]) if k in "1234567890"])
                        j = sorted([str(k) for k in str(stringrep) if k in "1234567890"])
                        while len(i) > 1:
                            i.insert(0, i.pop(0) + i.pop(0))
                        while len(j) > 1:
                            j.insert(0, j.pop(0) + j.pop(0))
#                        print i, j
                        if i == j:
                            print len(queue), str(current[0][0]) + ": " + answers[str(current)][0] + "\n",
                            writefile.write(str(current[0][0]) + ": " + answers[str(current)][0] + "\n")
#            print curscore, len(queue), current,
            current = [Fraction(i[0], i[1]) for i in current]
#            print answers[str([(k.numerator, k.denominator) for k in current])]
            for i in range(len(current)):
                # sqrt
                temp = copy(current)
                tempstr = copy(stringrep)
                if is_square(temp[i].numerator) and is_square(temp[i].denominator):
                    temp[i] = Fraction(-isqrt(temp[i].numerator), isqrt(temp[i].denominator))
                    tempstr.insert(i, "-sqrt(" + tempstr.pop(i) + ")")
                    if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                        heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                        answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                # Factorial
                temp = copy(current)
                tempstr = copy(stringrep)
                try:
                    if temp[i].numerator >= 0 and temp[i].numerator < 20 and temp[i].denominator == 1:
                        temp.insert(i, Fraction(-factorials[temp.pop(i).numerator], 1))
                        tempstr.insert(i, "-(" + tempstr.pop(i) + ")! ")
                        if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                            heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                            answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                except:
                    pass
                # sqrt
                temp = copy(current)
                tempstr = copy(stringrep)
                try:
                    if is_square(temp[i].numerator) and is_square(temp[i].denominator):
                        temp[i] = Fraction(isqrt(temp[i].numerator), isqrt(temp[i].denominator))
                        tempstr.insert(i, "sqrt(" + tempstr.pop(i) + ")")
#                        print temp
                        if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                            heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                            answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                except:
                    pass
                # Factorial
                temp = copy(current)
                tempstr = copy(stringrep)
                try:
                    if temp[i].numerator >= 0 and temp[i].numerator < 25 and temp[i].denominator == 1:
                        temp.insert(i, Fraction(factorials[temp.pop(i).numerator], 1))
                        tempstr.insert(i, "(" + tempstr.pop(i) + ")! ")
                        if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                            heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                            answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                except:
                    pass
            for i in range(len(current) - 1):
                # Exponents
                try:
                  temp = copy(current)
                  tempstr = copy(stringrep)
                  signal.signal(signal.SIGALRM, donothingandlikeit)
                  signal.alarm(2)
                  if abs(temp[i + 1]) * log(abs(temp[i])) / log(10) <= log(upperlimit) / log(10) + 1:
                   if abs(temp[i + 1]) * log(abs(temp[i].denominator)) / log(10) <= log(upperlimit) / log(10) + 1:
                    temp.insert(i, temp.pop(i) ** temp.pop(i))
                    tempstr.insert(i, "(" + tempstr.pop(i) + " ^ " + tempstr.pop(i) + ")")
                    if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                        heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                        answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                except BaseException as e:
#                    print e
                    pass
                signal.alarm(0)
                # Division
                temp = copy(current)
                tempstr = copy(stringrep)
                try:
                    temp.insert(i, temp.pop(i) / temp.pop(i))
                    tempstr.insert(i, "(" + tempstr.pop(i) + " / " + tempstr.pop(i) + ")")
                    if temp[i].denominator == 1:
                        if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                            heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                            answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                except:
                    pass
                # Multiplication
                temp = copy(current)
                tempstr = copy(stringrep)
                temp.insert(i, temp.pop(i) * temp.pop(i))
                tempstr.insert(i, "(" + tempstr.pop(i) + " * " + tempstr.pop(i) + ")")
                if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                    heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                    answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                # Subtraction
                temp = copy(current)
                tempstr = copy(stringrep)
                temp.insert(i, temp.pop(i) - temp.pop(i))
                tempstr.insert(i, "(" + tempstr.pop(i) + " - " + tempstr.pop(i) + ")")
                if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                    heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                    answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
                # Addition
                temp = copy(current)
                tempstr = copy(stringrep)
                temp.insert(i, temp.pop(i) + temp.pop(i))
                tempstr.insert(i, "(" + tempstr.pop(i) + " + " + tempstr.pop(i) + ")")
                if str([(k.numerator, k.denominator) for k in temp]) not in answers:
                    heapq.heappush(queue, (score(tempstr), [(k.numerator, k.denominator) for k in temp]))
                    answers[str([(k.numerator, k.denominator) for k in temp])] = tempstr
