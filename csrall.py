from math import log10
from copy import deepcopy as copy
from itertools import permutations

upperlimit = 10 ** 10

def is_square(i):
    if i < 2:
        return False
    sqrtp = 1
    upper = i
    lower = 1
    while upper > lower + 1:
        sqrtp = (upper + lower) / 2
#        print sqrtp
        if sqrtp * sqrtp < i:
            lower = sqrtp
        else:
            upper = sqrtp
    if sqrtp * sqrtp == i:
        return True
    return False

def sqrt(i):
    if i < 2:
        return False
    sqrtp = 1
    upper = i
    lower = 1
    while upper > lower + 1:
        sqrtp = (upper + lower) / 2
#        print sqrtp
        if sqrtp * sqrtp < i:
            lower = sqrtp
        else:
            upper = sqrtp
    if sqrtp * sqrtp == i:
        return sqrtp

def fac(i):
    if i == 0:
        return 1
    if i == 2:
        return 2
    answer = 1
    while i:
        answer *= i
        i -= 1
    return answer

def prodconcat(alist):
#    print alist
    answers = [str(alist)]
    i = 0
    while i < len(answers):
        for j in range(len(eval(answers[i])) - 1):
            temp = eval(answers[i])
            temp.insert(j, int(str(temp.pop(j)) + str(temp.pop(j))))
            if str(temp) not in answers:
                answers.append(str(temp))
        i += 1
    return [eval(i) for i in list(set(answers))]

def gennegs(alist):
    answers = [str(alist)]
    i = 0
    for i in range(2 ** len(alist)):
        temp = copy(alist)
        for j in range(len(alist)):
            if i & (2 ** j):
                temp[j] *= -1
        if str(temp) not in answers:
            answers.append(str(temp))
    return [eval(i) for i in list(set(answers))]
    
queue = []
for i in range(1, 10):
    for j in permutations(range(10), i):
      if len(j) > 1:
        seen = set()
        seen.add(str([k for k in j]))
#        print j
        for k in prodconcat(list(j)):
         try:
            for l in gennegs(k):
               if l[0] != 0:
                queue = [[str(m) for m in l]]
                while len(queue):
                    current = queue.pop()
                    seen.add(str([eval(o) for o in current]))
                    if len(current) == 1:
#                        print current
                        crap = "".join([m for m in current[0] if m in "0123456789"])
                        while len(crap) > 0 and crap[0] == "0":
                            crap = crap[1:]
                        if len(crap) == 0:
                            crap = "0"
#                        print current, "!!!", crap
                        if str(eval(current[0])) == crap and str(current[0]) != crap:
                            print eval(current[0]), current[0]
                            1/0
                    else:
                        for m in range(len(current) - 1):
                            temp = copy(current)
                            temp.insert(m, "-(" + temp.pop(m) + " * " + temp.pop(m) + ")")
                            queue.append(temp)
                        for m in range(len(current) - 1):
                            temp = copy(current)
                            temp.insert(m, "(" + temp.pop(m) + " - " + temp.pop(m) + ")")
                            queue.append(temp)
                        for m in range(len(current)):
                            temp = copy(current)
#                            print temp[m]
                            if eval(temp[m]) > 1 and is_square(eval(temp[m])):
                                temp.insert(m, "sqrt(" + temp.pop(m) + ")")
                                queue.append(temp)
                            temp = copy(current)
                            if eval(temp[m]) < 30 and eval(temp[m]) >= 0 and eval(temp[m]) != 0 and eval(temp[m]) != 2 and eval(temp[m]) != 1:
                                temp.insert(m, "fac(" + temp.pop(m) + ")")
                                queue.append(temp)
                        for m in range(len(current) - 1):
                            temp = copy(current)
                            if eval(temp[m+1]) > 0 and eval(temp[m]) % eval(temp[m + 1]) == 0:
                                temp.insert(m, "(" + temp.pop(m) + " / " + temp.pop(m) + ")")
                                queue.append(temp)
                        for m in range(len(current) - 1):
                            temp = copy(current)
                            if eval(temp[m+1]) > 0 and eval(temp[m]) % eval(temp[m + 1]) == 0:
                                temp.insert(m, "-(" + temp.pop(m) + " / " + temp.pop(m) + ")")
                                queue.append(temp)
                        for m in range(len(current) - 1):
                            temp = copy(current)
                            if eval(temp[m + 1]) >= 0:
                                if eval(temp[m]) >= 1:
                                    if eval(temp[m + 1]) * log10(eval(temp[m])) <= log10(upperlimit):
                                        temp.insert(m, "(" + temp.pop(m) + " ** " + temp.pop(m) + ")")
                                        queue.append(temp)
                            temp = copy(current)
                            temp.insert(m, "(" + temp.pop(m) + " * " + temp.pop(m) + ")")
                            queue.append(temp)
                            temp = copy(current)
                            temp.insert(m, "(" + temp.pop(m) + " + " + temp.pop(m) + ")")
                            queue.append(temp)
                while len(queue) > 0 and str([eval(o) for o in queue[-1]]) in seen:
                    queue.pop()
         except:
                pass     