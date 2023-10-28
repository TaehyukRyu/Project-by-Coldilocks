import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.cluster import DBSCAN
import telegram, asyncio
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import matplotlib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import matplotlib

SOPR_df = pd.read_excel('SOPR 비율.xlsx')

try:
    SOPR_df['날짜'] = pd.to_datetime(SOPR_df['날짜'])
    SOPR_df['가격'] = SOPR_df['가격'].str.replace(',', '').astype(float)
except:
    pass

scaler = MinMaxScaler()
SOPR_df[['SOPR 비율 (장기 보유자 SOPR/단기 보유자 SOPR)']] = scaler.fit_transform(SOPR_df[['SOPR 비율 (장기 보유자 SOPR/단기 보유자 SOPR)']])

# Isolation Forest 모델 생성 및 학습
model = IsolationForest(contamination=0.02)  # contamination 파라미터는 이상치의 비율을 설정합니다.
model.fit(SOPR_df[['SOPR 비율 (장기 보유자 SOPR/단기 보유자 SOPR)']])

# 각 포인트가 이상치인지 아닌지 판별합니다.
SOPR_df['anomaly'] = model.predict(SOPR_df[['SOPR 비율 (장기 보유자 SOPR/단기 보유자 SOPR)']])

print(len(SOPR_df[SOPR_df['anomaly']==-1]))

# SOPR_last_label = SOPR_df.iloc[-1]['anomaly']

