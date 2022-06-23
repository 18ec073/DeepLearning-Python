# 売買シミュレーション(2012年〜2021年)
import pandas as pd

sp = 0 # スプレッド
rigui = 30 # 利食い開始値30
songiri = 500 # 損切り値500
alpha = 0.96 # α%
sum = 2000 * 10 ** 4 # 総資金
max = 0 # 最大値
min = 0 # 最小値
positionlist = [None, None]
count = 0 # シミュレーション回数
sumlist = [2000 * 10 ** 4] # 資金配列
GUIsumlist = [] # GUI用資金配列
win = 0 # 勝ち数
loose = 0 # 負け数
daylist = ['2017年12月29日', '2018年12月28日', '2019年12月30日']
winlist = []
looselist = []
lastday = False
ryoudate_count = 0
ryoudatelist = []
tesuuryou = 300*1.1 # 手数料
ratio = 0.2 # 売買に使用する総資金の割合
bairitulist = []
sum_before = sum
t = None
typelist = []
lt = 0 #最後の日のカウント
daylt = 0 #最後の日のカウント

day1=[]#データの日付
owarine1=[]#終値
hajimene1=[]#始値
takane1=[]#高値
yasune1=[]#安値
day=[]#予測日付
jyousyou=[]#予測上昇度

file1=pd.read_csv('2017-2019-sakimono.csv',delimiter=',',encoding="shift-jis")#時系列データ
for i in range(len(file1)):
    day1.append(file1['日付'][i]) #日付
    owarine1.append(file1['終値'][i]) #終値
    hajimene1.append(file1['始値'][i])#始値
    takane1.append(file1['高値'][i])#高値
    yasune1.append(file1['安値'][i])#安値


with open("yosoku2t.txt","r",encoding="utf-8") as f: #予測データ
    next(f)
    for line in f:
        data2 = line.split(' ')
        day.append(str(data2[0]))#日付
        jyousyou.append(str(data2[1]))#予測上昇度

d=0
while(day1[d]!=day[0]):#日付合わせ
    d+=1
day2=[]
hajimene=[]
owarine2=[]
takane=[]
yasune=[]

for i in range(0,len(day),+1):#データの日付を予測の日付に合わせる
    day2.append(day1[d])
    hajimene.append(hajimene1[d])
    owarine2.append(owarine1[d])
    takane.append(takane1[d])
    yasune.append(yasune1[d])
    d+=1

# 両建て
for i in range(len(day2) - 1):
    #買い
    if(positionlist[0] == None):
        if(int(jyousyou[i]) == 1):
            owarine = owarine2[i] + sp
            cnt = int((sum * ratio) / owarine)
            positionlist[0] = [owarine, cnt] # 買い
            sum -= tesuuryou * cnt
            #max = takane[i]
            max = positionlist[0][0]
            count += 1
            #print("1")
            #typelist.append(1)
        #else:
            #typelist.append(4)

    elif(positionlist[0] != None):
        if(int(jyousyou[i]) == 0):
            if(max < takane[i]):
                max = takane[i]
            if(positionlist[0][0] - songiri <= takane[i]):
                if(positionlist[0][0] - songiri >= yasune[i]):
                    b = (-songiri - sp) * positionlist[0][1] # 損切り
                    sum += b
                    loose += 1
                    count += 1
                    positionlist[0] = None
                    #t = 2
                    #print("2")
                elif(positionlist[0][0] - songiri >= hajimene[i+1]):
                    b = (hajimene[i+1] - positionlist[0][0] - sp) * positionlist[0][1] # 損切り
                    sum += b
                    loose += 1
                    count += 1
                    positionlist[0] = None
                    #t = 2
                    #print("3")
            if(positionlist[0] != None):
                if(rigui <= max - positionlist[0][0]):
                    if((max - positionlist[0][0]) * alpha + positionlist[0][0] <= takane[i]):
                        if((max - positionlist[0][0]) * alpha + positionlist[0][0] >= yasune[i]):
                            b = ((max - positionlist[0][0]) * alpha - sp) * positionlist[0][1] # 利食い
                            sum += b
                            win += 1
                            count += 1
                            positionlist[0] = None
                            #t = 3
                            #print("4")
                        elif((max - positionlist[0][0]) * alpha + positionlist[0][0] >= hajimene[i+1]):
                            b = (hajimene[i+1] - positionlist[0][0] - sp) * positionlist[0][1] # 利食い
                            sum += b
                            win += 1
                            count += 1
                            positionlist[0] = None
                            #t = 3
                            #print("5")

        #if(t == None):
            #typelist.append(4)
        #else:
            #typelist.append(t)
            #t = None

    #売り
    if(positionlist[1] == None):
        if(int(jyousyou[i]) == 0):
            owarine = owarine2[i] - sp
            cnt = int((sum * ratio) / owarine)
            positionlist[1] = [owarine, cnt] # 売り
            sum -= tesuuryou * cnt
            #min = yasune[i]
            min = positionlist[1][0]
            count += 1
            #print("6")
    elif(positionlist[1] != None):
        if(int(jyousyou[i]) == 1):
            if(min > yasune[i]):
                min = yasune[i]
            if(positionlist[1][0] + songiri >= yasune[i]):
                if(positionlist[1][0] + songiri <= takane[i]):
                    b = (-songiri - sp) * positionlist[1][1] # 損切り
                    sum += b
                    loose += 1
                    count += 1
                    positionlist[1] = None
                    #print("7")
                elif(positionlist[1][0] + songiri <= hajimene[i+1]):
                    b = (positionlist[1][0] - hajimene[i+1] - sp) * positionlist[1][1] # 損切り
                    sum += b
                    loose += 1
                    count += 1
                    positionlist[1] = None
                    #print("8")
            if(positionlist[1] != None):
                if(rigui <= positionlist[1][0] - min):
                    if(positionlist[1][0] - (positionlist[1][0] - min) * alpha >= yasune[i]):
                        if(positionlist[1][0] - (positionlist[1][0] - min) * alpha <= takane[i]):
                            b = ((positionlist[1][0] - min) * alpha - sp) * positionlist[1][1] # 利食い
                            sum += b
                            win += 1
                            count += 1
                            positionlist[1] = None
                            #print("9")
                        elif(positionlist[1][0] - (positionlist[1][0] - min) * alpha <= hajimene[i+1]):
                            b = (positionlist[1][0] - hajimene[i+1] - sp) * positionlist[1][1] # 利食い
                            sum += b
                            win += 1
                            count += 1
                            positionlist[1] = None
                            #print("10")

    if(positionlist[0] != None and positionlist[1] != None):
        ryoudate_count += 1

    sumlist.append(sum)

    if(day2[i] == day[daylt]):
            lt += 1
            if(lt == 62):
                lastday = True
                lt = 0
                daylt += 1

    if(lastday == True):
        winlist.append(win)
        looselist.append(loose)
        GUIsumlist.append(sum)
        ryoudatelist.append(ryoudate_count)
        bairitulist.append(float(sum / sum_before))
        sum_before = sum
        win = 0
        loose = 0
        ryoudate_count = 0
        lastday = False

f = open("filezimaeT.csv", "w", encoding="shift_jis")
for i in range(len(day2)):
    f.write(str(day2[i])+","+str(sumlist[i])+","+str(jyousyou[i])+"\n")
f.write('計：'+","+str(sum))
f.close()
print(count)
print(winlist)
print(looselist)
print(GUIsumlist)
print(ryoudatelist)
print(bairitulist)
