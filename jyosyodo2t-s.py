import pandas as pd

s = open('Jyousyoudo2t.txt','w',encoding="utf-8") #上昇度ファイル生成
s.write("日付 上昇度"+"\n")
d = open("jyousyoudoonly2.txt","w",encoding="utf-8")

day1 = []#日付

file=pd.read_csv('Y2014-2019all-notime.csv',delimiter=',',encoding="shift-jis")#デューカスデータ
for i in range(len(file)):
    day1.append(file['日付け'][i])


data2 = []#日付と天底の分割
day2 = []#sp波動法の日付
teiten = []#天井と底
with open("sp2t.txt","r",encoding="utf-8") as f:#SP波動法
    next(f)
    for line in f:
        data2 = line.split()
        day2.append(str(data2[0]))
        teiten.append(int(data2[1]))



a = 0
b = 0
while (day1[a] != day2[b]):#日付合わせ
    a=a+1


s.write(str(day1[a])+" "+str(teiten[b])+"\n")
b=b+1
day2.append(0)
teiten.append(0)

for i in range(a+1,len(day1),1):
    if(day1[i] == day2[-2]):
        s.write(str(day1[i])+" "+str(teiten[b])+"\n")
        d.write(str(teiten[b])+"\n")
        break
    elif(day1[i] == day2[b]):
        s.write(str(day1[i])+" "+str(teiten[b])+"\n")
        d.write(str(teiten[b])+"\n")
        b+=1
    else:
        s.write(str(day1[i])+" "+str(teiten[b])+"\n")
        d.write(str(teiten[b])+"\n")

s.close()
d.close()
