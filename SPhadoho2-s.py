import numpy as np
import pandas as pd

sp = 2.0#1.5#任意に値決める(SP波動法の値)
day = []#日付
owarine = []#終値
data2 = []#日付、終値
ten = 0#天井
tei = 0#底
result = []#sp波動法で求めた結果

file=pd.read_csv('Y2014-2019all-notime.csv',delimiter=',',encoding="shift-jis")
for i in range(len(file)):
    day.append(file['日付け'][i])
    owarine.append(file['終値'][i])

for i in range(len(day)):
    set1 = []
    set1.append(day[i])
    set1.append(owarine[i])
    data2.append(set1)

def bottom(x):#底求める
    y = ten*(200-sp)/(200+sp)
    if(owarine[x] < y):
        return 1
    return 0

def top(x):#天井求める
    y = tei*(200+sp)/(200-sp)
    if(owarine[x] > y):
        return 1
    return 0

saidai = np.argmax(owarine)#データの中で最大値(天井)
result.append(data2[saidai])
a = saidai
ten = owarine[saidai]
mode = 0

for i in range(saidai,-1,-1):#最大値(天井)から左側

    if mode == 0:
        if (bottom(i) == 1):
            tei = owarine[i]
            a = owarine.index(owarine[i])
            result.append([data2[i],0])
            mode = 1
        elif (owarine[i] >= ten):
            ten = owarine[i]
            a = owarine.index(owarine[i])
            result.pop()
            result.append([data2[i],1])

    if mode == 1:
        if (top(i) == 1):
            ten = owarine[i]
            a = owarine.index(owarine[i])
            result.append([data2[i],1])
            mode = 0
        elif (owarine[i] <= tei):
            tei = owarine[i]
            a = owarine.index(owarine[i])
            result.pop()
            result.append([data2[i],0])

result.pop()
result.reverse()
a = saidai
ten = owarine[saidai]
mode = 0

for i in range(saidai,len(owarine),1):#最大値(天井)から右側

    if mode == 0:
        if (bottom(i) == 1):
            tei = owarine[i]
            a = owarine.index(owarine[i])
            result.append([data2[i],0])
            mode = 1
        elif (owarine[i] > ten):
            ten = owarine[i]
            a = owarine.index(owarine[i])
            result.pop()
            result.append([data2[i],1])

    if mode == 1:
        if (top(i) == 1):
            ten = owarine[i]
            a = owarine.index(owarine[i])
            result.append([data2[i],1])
            mode = 0
        elif (owarine[i] < tei):
            tei = owarine[i]
            a = owarine.index(owarine[i])
            result.pop()
            result.append([data2[i],0])

result.pop()

s = open("sp2t.txt","w",encoding="utf-8")
s.write("日付　天井と底"+"\n")

for i in range (0,len(result),1):
    s.write(str(result[i][0][0])+" "+str(result[i][1])+"\n")

s.close()
