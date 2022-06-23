import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from tensorflow.keras import optimizers
from sklearn.model_selection import train_test_split
import pandas as pd


data=[]#予測に用いる長さの時系列データ群
data2 = []#分割
target = []#予測によって得られるべきデータ群
kairi = []#乖離率
jyousyou = []#上昇度
maxlen = 60#移動平均線と同じ値にしている
day1 = []#データの日付
day2 = []#乖離率の日付
day3 = []#上昇度の日付

def normalization(a):#正規化
    b = []
    for i in a:
        b.append((i-min(a))/(max(a)-min(a)))
    return b


owarine = []#終値

file=pd.read_csv('Y2014-all-notime.csv',delimiter=',',encoding="shift-jis")
for i in range(len(file)):
    day1.append(file['日付け'][i]) #日付
    owarine.append(file['終値'][i]) #終値

with open("kairiritu2t.txt","r",encoding="utf-8") as f:
    next(f)
    for line in f:
        data2 = line.split(' ')
        day2.append(str(data2[0])) #日付
        kairi.append(float(data2[2])) #乖離率

with open("Jyousyoudo2t.txt","r",encoding="utf-8") as f:
    next(f)
    for line in f:
        data3 = line.split(' ')
        day3.append(str(data3[0])) #日付
        jyousyou.append(float(data3[1])) #上昇度



'''
日付合わせ
'''
for i in range(len(owarine)-1,0,-1):
    if(day1[i] == day3[-1]):
        del day1[i+1:len(day1)]
        del owarine[i+1:len(owarine)]
        break
for i in range(len(kairi)-1,0,-1):
    if(day2[i] == day3[-1]):
        del day2[i+1:len(day2)]
        del kairi[i+1:len(kairi)]
        break

if(len(day2) > len(day3)):
    for i in range(0,len(owarine)):
        if(day1[i] == day3[0]):
            del day1[0:i]
            del owarine[0:i]
            break
    for i in range(0,len(kairi)-1):
        if(day2[i] == day3[0]):
            del day2[0:i]
            del kairi[0:i]
            break
else:
    for i in range(0,len(owarine)):
        if(day1[i] == day2[0]):
            del day1[0:i]
            del owarine[0:i]
            break
    for i in range(0,len(jyousyou)):
        if(day3[i] == day2[0]):
            del day3[0:i]
            del jyousyou[0:i]
            break

'''
日付のチェック
'''
print (day1[0])
print (day2[0])
print (day3[0])
print (day1[-1])
print (day2[-1])
print (day3[-1])
print (len(day1),len(day2),len(day3))
print (len(owarine),len(kairi),len(jyousyou))


for i in range(0, len(kairi)-maxlen):
    data.append(normalization(kairi[i: i + maxlen]))
    target.append(jyousyou[i + maxlen - 1])
    if((i + maxlen - 1)==(len(jyousyou) - 1)):
            break

X = np.array(data).reshape(len(data), maxlen, 1)
Y = np.array(target).reshape(len(data), 1)

# データ設定
N_train = int(len(data) * 0.5)#学習期間5割(任意)
N_validation = len(data) - N_train

X_train, X_validation, Y_train, Y_validation = \
    train_test_split(X, Y, test_size=N_validation,shuffle=False)

'''
モデル設定
'''
n_in = len(X[0][0])#入力層
n_hidden = 60#中間層
n_out = len(Y[0])#隠れ層


model = Sequential()
model.add(LSTM(n_hidden,
                    kernel_initializer="random_uniform",
                    input_shape=(maxlen, n_in)))#LSTM

model.add(Dense(n_hidden, kernel_initializer="random_uniform"))
model.add(Activation('sigmoid'))

model.add(Dense(n_out, kernel_initializer="random_uniform"))
model.add(Activation('sigmoid'))

optimizer = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
model.compile(loss='mean_squared_error',
              optimizer=optimizer, metrics = ['accuracy'])

'''
モデル学習
'''
epochs = 100#任意
batch_size = 1000#任意

model.fit(X_train, Y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_split = 0.25)



y_ = model.predict(X_validation)

yosoku = []#予測結果


for i in range (0,len(y_)):
    if (y_[i]>=0.5):
        yosoku.append('1')
    else :
        yosoku.append('0')


b = open("yosoku2t.txt","w",encoding="utf-8")
b.write("日付 上昇度" + "\n")
print(len(yosoku))
for s in range(len(yosoku)):
    b.write(str(day3[(len(jyousyou))-(len(yosoku))+s])+" "+str(yosoku[s])+"\n")
b.close()

c = open("yosokuonlyt.txt","w",encoding="utf-8")
for s in range(len(yosoku)):
    c.write(str(yosoku[s])+"\n")
c.close()
