from math import log10
from copy import deepcopy as copy
from multiprocessing import Pool
import shelve
upperlimit = 1000000000
number_of_processes = 4

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
    sqrtp += 1
    if sqrtp * sqrtp == i:
        return True
    return False

def fac(i):
    answer = 1
    while i > 0:
        answer *= i
        i -= 1
    return answer

def recur(numbers, strings):
    numbers = eval(numbers)
    answers = []
    for i in range(len(numbers)):
        # Unary Minus
        temp1 = copy(numbers)
        temp2 = copy(strings)
        temp1.insert(i, temp1.pop(i) * -1)
        temp2.insert(i, "-(" + temp2.pop(i) + ")")
        answers.append((temp1, temp2))
        # Factorial
        temp1 = copy(numbers)
        temp2 = copy(strings)
        if temp1[i] == 0 or (temp1[i] > 2 and temp1[i] < 30):
            temp1.insert(i, fac(temp1.pop(i)))
            temp2.insert(i, "(" + temp2.pop(i) + ")!")
            answers.append((temp1, temp2))
#        # Square Root
#        temp1 = copy(numbers)
#        temp2 = copy(strings)
#        if is_square(temp1[i]):
#            temp1.insert(i, int(temp1.pop(i) ** .5))
#            temp2.insert(i, "sqrt(" + temp2.pop(i) + ")")
#            answers.append((temp1, temp2))
    for i in range(len(numbers) - 1):
        # Addition
        temp1 = copy(numbers)
        temp2 = copy(strings)
        temp1.insert(i, temp1.pop(i) + temp1.pop(i))
        temp2.insert(i, "(" + temp2.pop(i) + " + " + temp2.pop(i) + ")")
        answers.append((temp1, temp2))
        # Subtraction
        temp1 = copy(numbers)
        temp2 = copy(strings)
        temp1.insert(i, temp1.pop(i) - temp1.pop(i))
        temp2.insert(i, "(" + temp2.pop(i) + " - " + temp2.pop(i) + ")")
        answers.append((temp1, temp2))
        # Multiplication
        temp1 = copy(numbers)
        temp2 = copy(strings)
        temp1.insert(i, temp1.pop(i) * temp1.pop(i))
        temp2.insert(i, "(" + temp2.pop(i) + " * " + temp2.pop(i) + ")")
        answers.append((temp1, temp2))
        # Division
        temp1 = copy(numbers)
        temp2 = copy(strings)
        if temp1[i + 1] > 1 and temp1[i] % temp1[i + 1] == 0:
            temp1.insert(i, temp1.pop(i) / temp1.pop(i))
            temp2.insert(i, "(" + temp2.pop(i) + " / " + temp2.pop(i) + ")")
            answers.append((temp1, temp2))
        # Exponents
        temp1 = copy(numbers)
        temp2 = copy(strings)
        if temp1[i] != 0 and temp1[i + 1] > 1 and temp1[i + 1] * log10(abs(temp1[i])) < log10(upperlimit):
            temp1.insert(i, temp1.pop(i) ** temp1.pop(i))
            temp2.insert(i, "(" + temp2.pop(i) + " ^ " + temp2.pop(i) + ")")
            answers.append((temp1, temp2))
    i = 0
    while i < len(answers):
        good = True
        for j in answers[i][0]:
            if abs(j) > upperlimit:
                good = False
        if good:
            i += 1
        else:
            answers.pop(i)
#    for i in answers:
#        print i
    return answers

if __name__ == "__main__":
    answers = dict()
    pool = Pool(processes = number_of_processes)
    iii = 10
    for iii in [123456789, 987654321]:
#    while iii < 10 ** 10:
#    while iii < 40:
        seen = shelve.open("seen" + str(iii) + ".txt")
        queue = shelve.open("queue" + str(iii) + ".txt")
        queues = [[[int(i) for i in str(iii)], [j for j in str(iii)]]]
        jj = 0
        while jj < len(queues):
            for kk in range(len(queues[jj][0]) - 1):
                temp = copy(queues[jj])
                if temp[0][kk] != 0:
                    temp[0].insert(kk, int(str(temp[0].pop(kk)) + str(temp[0].pop(kk))))
                    temp[1].insert(kk, (str(temp[1].pop(kk)) + str(temp[1].pop(kk))))
                    if temp not in queues:
                        queues.append(temp)                
            jj += 1
        for (ii, jj) in queues:
#            print ii, jj
            if len(ii) > 1:
                queue[str(ii)] = jj
#        queue[str([1,2,3,4,5,6,7,8,9])] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        done = False
        while not done:
#            print iii, len(seen), "/", len(queue), "\r",
            done = True
            results = []
            for h in [i for i in queue if i not in seen][:1024]:
#            for h in [i for i in queue if i not in seen][:number_of_processes ** 2]:
#                if h not in seen:
                    seen[h] = True
                    results.append(pool.apply_async(recur, (h, queue[h])))
#                del queue[h]
#            print len(results)
            while len(results) > 0:
                for k in results.pop().get():
#                    print k, [i for i in seen]
                    if str(k[0]) not in queue:
                        queue[str(k[0])] = k[1]
#                        if len(eval(k[0])) == 1:
                        if len(k[1]) == 1:
#                            if str(k[0][0]) == "".join([kk for kk in k[1][0] if kk in "0123456789"]):
#                                print k
#                            if str(k[0][0])[::-1] == "".join([kk for kk in k[1][0] if kk in "0123456789"]):
##                                print [k if k[0][0] >= 0 else ""]
                                if (k[0][0] not in answers) or (len(answers[k[0][0]]) > len(str(k))):
                                    answers[k[0][0]] = str(k)
                    done = False
        seen.close()
        queue.close()
        while len(answers) > 0:
            temp = min(answers)
            if temp >= 0:
                print answers[temp]
            del answers[temp]
        iii += 1
