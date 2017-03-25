import csv
import numpy as np
import pickle
import random

# 3rd party
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import seaborn as sns

sns.set_color_codes()
sns.set_style("white")

dfvisual = pd.read_csv('/Users/awei/Documents/Baller-Shot-Caller/Visual_Game/df4plot1.csv')

rnd = random.randint(0,len(dfvisual.index)-1)

'''Danny Green'''
DGlstx = []
DGlsty = []
DGlstname = []

i=3
count = 0
while count < 30:
    DGlstx.append(i)
    i += 5
    count += 1

i = 153
count = 0
while count < 30:
    DGlsty.append(i)
    i += 5
    count += 1

count = 0
while count < 30:
    DGlstname.append("Danny Green")
    count += 1

DGlstxv = []
DGlstyv = []

for i in DGlstx:
    DGlstxv.append(dfvisual.iloc[rnd,i])

for i in DGlsty:
    DGlstyv.append(dfvisual.iloc[rnd,i])

dfDG = pd.DataFrame([DGlstname, DGlstxv, DGlstyv]).T

'''Tim Duncan'''
TDlstx = []
TDlsty = []
TDlstname = []

i=6
count = 0
while count < 30:
    TDlstx.append(i)
    i += 5
    count += 1

i = 156
count = 0
while count < 30:
    TDlsty.append(i)
    i += 5
    count += 1

count = 0
while count < 30:
    TDlstname.append("Tim Duncan")
    count += 1

TDlstxv = []
TDlstyv = []

for i in TDlstx:
    TDlstxv.append(dfvisual.iloc[rnd,i])

for i in TDlsty:
    TDlstyv.append(dfvisual.iloc[rnd,i])

dfTD = pd.DataFrame([TDlstname, TDlstxv, TDlstyv]).T

'''Kawhi Leonard'''
KLlstx = []
KLlsty = []
KLlstname = []

i=4
count = 0
while count < 30:
    KLlstx.append(i)
    i += 5
    count += 1

i = 154
count = 0
while count < 30:
    KLlsty.append(i)
    i += 5
    count += 1

count = 0
while count < 30:
    KLlstname.append("Kawhi Leonard")
    count += 1

KLlstxv = []
KLlstyv = []

for i in KLlstx:
    KLlstxv.append(dfvisual.iloc[rnd,i])

for i in KLlsty:
    KLlstyv.append(dfvisual.iloc[rnd,i])

dfKL = pd.DataFrame([KLlstname, KLlstxv, KLlstyv]).T

'''LaMarcus Aldridge'''
LAlstx = []
LAlsty = []
LAlstname = []

i=5
count = 0
while count < 30:
    LAlstx.append(i)
    i += 5
    count += 1

i = 155
count = 0
while count < 30:
    LAlsty.append(i)
    i += 5
    count += 1

count = 0
while count < 30:
    LAlstname.append("LaMarcus Aldridge")
    count += 1

LAlstxv = []
LAlstyv = []

for i in LAlstx:
    LAlstxv.append(dfvisual.iloc[rnd,i])

for i in LAlsty:
    LAlstyv.append(dfvisual.iloc[rnd,i])

dfLA = pd.DataFrame([LAlstname, LAlstxv, LAlstyv]).T

'''Tony Parker'''
TPlstx = []
TPlsty = []
TPlstname = []

i=7
count = 0
while count < 30:
    TPlstx.append(i)
    i += 5
    count += 1

i = 157
count = 0
while count < 30:
    TPlsty.append(i)
    i += 5
    count += 1

count = 0
while count < 30:
    TPlstname.append("Tony Parker")
    count += 1

TPlstxv = []
TPlstyv = []

for i in TPlstx:
    TPlstxv.append(dfvisual.iloc[rnd,i])

for i in TPlsty:
    TPlstyv.append(dfvisual.iloc[rnd,i])

dfTP = pd.DataFrame([TPlstname, TPlstxv, TPlstyv]).T

"""Creating DataFrame for visual"""
df_plt = pd.concat([dfDG, dfTD, dfKL,dfLA,dfTP], axis=1)
df_plt.to_csv('/Users/awei/Documents/Baller-Shot-Caller/Visual_Game/df4plot2.csv')

"""Creating Plot"""
DGx,DGy, TDx, TDy, KLx, KLy, LAx, LAy,TPx,TPy=np.loadtxt('/Users/khalilezzine/Desktop/DS/Visual_Game/df4plot2.csv',unpack=True,
                delimiter=',',skiprows=1,usecols=(2,3,5,6,8,9,11,12,14,15))
court=plt.imread("/Users/awei/Documents/Baller-Shot-Caller/Visual_Game/fullcourt.png")
plt.figure(figsize=(15,11.5))

plt.imshow(court, zorder=0, extent=[0,94,50,0])
plt.xlim(0,101)

plt.plot(DGx,DGy, color='r', linewidth=5.0)
plt.plot(TDx,TDy, color='b', linewidth=5.0)
plt.plot(KLx,KLy, color='g', linewidth=5.0)
plt.plot(LAx,LAy, color='y', linewidth=5.0)
plt.plot(TPx,TPy, color='c', linewidth=5.0)

plt.show()
