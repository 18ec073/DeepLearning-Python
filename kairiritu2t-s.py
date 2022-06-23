import pandas as pd

date = []#日付
owari = []#終値
ma = []#移動平均線
kairi = []#乖離率
wa=0.0#移動平均線を求めるのに使う



file=pd.read_csv('Y2014-2019all-notime.csv',delimiter=',',encoding="shift-jis")

for i in range(len(file)):



    date.append(file['日付け'][i])
    owari.append(file['終値'][i])



for i in range(len(owari)+1):
    if i>=60:
        for j in range(i-60,i):
            wa +=owari[j]
        ma.append(wa/60) #移動平均線(60日)
        kairi.append(owari[i-1]/ma[i-60])
        wa=0

a = open("kairiritu2t.txt","w",encoding="utf-8")
a.write("日付 終値 乖離率" + "\n")
tyouka = 59 #乖離率(60日から表示するため)
for i in range(len(kairi)):
    a.write(str(date[tyouka])+" "+(str(owari[tyouka])+" "+(str(kairi[i])) + "\n"))
    tyouka += 1
a.close

a = open("kairirituonly2t.txt","w",encoding="utf-8")
tyouka = 59 #乖離率(60日から表示するため)
for i in range(len(kairi)):
    a.write(str(kairi[i]) + "\n")
    tyouka += 1
a.close

a = open("idouheikin2t.txt","w",encoding="utf-8")
tyouka = 59 #乖離率(60日から表示するため)
for i in range(len(kairi)):
    a.write(str(ma[i]) + "\n")
    tyouka += 1
a.close
print(date[-1])
