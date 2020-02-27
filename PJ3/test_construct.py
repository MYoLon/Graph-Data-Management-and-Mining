# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 11:14:47 2020

@author: yuansiyu
"""

from random import randint, sample

n = 2
m = 1
l = 5

D = {}
D[1] = 'A'
D[2] = 'B'
D[3] = 'C'
D[4] = 'D'
D[5] = 'E'
lines = [str(n) + '\t' + str(m) + '\n']
vertices = [D[randint(1,l)] + '\n' for i in range(n)]
lines.extend(vertices)

edges = []
i = 0
while i < m:
    A = str(randint(0,n-1))
    B = str(randint(0,n-1))
    if A != B:
        s = A + '\t' + B + '\t' + str(randint(1,1)) + '\n'
        if s not in edges:
            edges.append(A + '\t' + B + '\t' + str(randint(1,1)) + '\n')
            i = i + 1

lines.extend(edges)

fo = open('D:\\subdata.txt','w')
fo.writelines(lines)
fo.close()