import os
import sys
import numpy as np 
from numpy import array
import pandas as pd 
from sklearn import preprocessing

DATA_PATH = os.path.abspath(sys.argv[1])

df = pd.read_csv(DATA_PATH)

zeros_cnt = df.isnull().sum().sort_values(ascending=False)
percent_zeros = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)

missing_data = pd.concat([zeros_cnt, percent_zeros], axis=1, keys=['Total', 'Percent'])

dropList = list(missing_data[missing_data['Percent'] > 0.15].index)

df.drop(dropList, axis=1, inplace=True)
df.drop(['Date'], axis=1, inplace=True)
df.drop(['Location'], axis=1, inplace=True)

ohe = pd.get_dummies(data=df, columns=['WindGustDir','WindDir9am','WindDir3pm'])


ohe['RainToday'] = df['RainToday'].astype(str)
ohe['RainTomorrow'] = df['RainTomorrow'].astype(str)

lb = preprocessing.LabelBinarizer()

ohe['RainToday'] = lb.fit_transform(ohe['RainToday'])
ohe['RainTomorrow'] = lb.fit_transform(ohe['RainTomorrow'])
ohe = ohe.dropna()
precessed_df = ohe

y = ohe['RainTomorrow']
X = ohe.drop(['RainTomorrow'], axis=1)

cols = precessed_df.columns.tolist()
cols.remove('RainTomorrow')
cols.append('RainTomorrow')
precessed_df = precessed_df[cols]

cols = precessed_df.columns.tolist()

features_df = precessed_df.drop(['RainTomorrow'], axis=1)
features_df.to_csv("./data/features.csv", index=False)

precessed_df.to_csv(DATA_PATH[:-4]+"_processed.csv", index=False)
