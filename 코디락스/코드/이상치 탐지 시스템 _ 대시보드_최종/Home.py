import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time
import yfinance as yf
import datetime
import plotly.graph_objects as go
import ccxt
import requests
from bs4 import BeautifulSoup
import pandas as pd

def calculate_bollinger_bands(data, window=7, num_std_dev=2):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['Upper'] = data['SMA'] + (data['Close'].rolling(window=window).std() * num_std_dev)
    data['Lower'] = data['SMA'] - (data['Close'].rolling(window=window).std() * num_std_dev)
    data['BandWidth'] = (data['Upper'] - data['Lower']) / data['SMA']
    return data


st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#side bar
st.sidebar.image("data/logo1.png",caption="Developed and Maintaned by: samir: +255675839840")

# 텔레그램 링크를 사이드바에 추가
st.sidebar.markdown("[텔레그램](https://t.me/+8hSXtgL02rRhMTJl)")
st.sidebar.markdown("[크립토퀀트](https://cryptoquant.com/ko)")
st.sidebar.markdown("[coinsect](https://coinsect.io/indicators/leaderboard)")

# BTC 데이터를 저장할 변수 초기화
BTC_Price = 0
BTC_Change = 0
current_time = 0
col1, col2 = st.columns(2)

# 초기에 빈 공간을 생성합니다.
BTC_Price_info = col1.empty()
BTC_Price_placeholder = col1.empty()

Time_info = col2.empty()
Time_placeholder = col2.empty()

Chart = st.empty()

binance = ccxt.binance()

btc_data = binance.fetch_ohlcv("BTC/USDT", "1d", limit=1)

# 현재 가격 및 등락률 업데이트
BTC_Price = btc_data[0][4]
BTC_Open = btc_data[0][1]

col3, col4 = st.columns(2)

Indicator_info = col3.empty()
Indicator1 = col3.empty()
Indicator2 = col3.empty()
Indicator3 = col3.empty()

Leaderboard_info = col4.empty()
Leaderboard1 = col4.empty()

def leaderbord_df_update():
    # 웹 페이지 URL
    url = "https://coinsect.io/indicators/leaderboard"

    # 웹 페이지 내용 가져오기
    response = requests.get(url)
    html = response.text

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")

    # 원하는 테이블 선택 (CSS 선택자 사용)
    table = soup.select_one("#app > div.app-body.layout-centered > div > div.view-indicators > div > table")

    # 데이터 추출
    data = []
    header = []

    # 테이블의 헤더 추출
    for th in table.find_all("th"):
        header.append(th.text.strip())

    # 테이블의 각 행을 추출
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    # 데이터프레임 생성
    df = pd.DataFrame(data[1:], columns=header)
    df.to_excel("leaderboard_df.xlsx", index=False)

def bitcoin_df_update():
    # 현재 날짜 계산
    end_date = datetime.datetime.now().date()
    # 3년 전 날짜 계산
    start_date = end_date - datetime.timedelta(days=3 * 365)
    # 비트코인 데이터 가져오기
    bitcoin_df = yf.download('BTC-USD', start=start_date, progress=False)
    bitcoin_df.reset_index(inplace=True)

    mpi_df = pd.read_excel('채굴자 포지션 지표 (MPI).xlsx')
    Whale_df = pd.read_excel('거래소 고래 비율 (Exchange Whale Ratio).xlsx')
    Coinbase_df = pd.read_excel('코인베이스 프리미엄 지표.xlsx')

    mpi_df['Date'] = mpi_df['날짜']
    Whale_df['Date'] = Whale_df['날짜']
    Coinbase_df['Date'] = Coinbase_df['날짜']

    # 'Date'를 기준으로 두 데이터프레임을 조인하면서 'label'을 'mpi_label'로 변경
    bitcoin_df = pd.merge(bitcoin_df, mpi_df[['날짜', 'label']], left_on='Date', right_on='날짜', how='left')
    bitcoin_df.rename(columns={'label': 'Mpi_label'}, inplace=True)
    bitcoin_df.drop(columns=['날짜'], inplace=True)

    # 'Date'를 기준으로 두 데이터프레임을 조인하면서 'label'을 'mpi_label'로 변경
    bitcoin_df = pd.merge(bitcoin_df, Whale_df[['날짜', 'label']], left_on='Date', right_on='날짜', how='left')
    bitcoin_df.rename(columns={'label': 'Whale_label'}, inplace=True)
    bitcoin_df.drop(columns=['날짜'], inplace=True)

    # 'Date'를 기준으로 두 데이터프레임을 조인하면서 'label'을 'mpi_label'로 변경
    bitcoin_df = pd.merge(bitcoin_df, Coinbase_df[['날짜', 'anomaly']], left_on='Date', right_on='날짜', how='left')
    bitcoin_df.rename(columns={'anomaly': 'Coinbase_label'}, inplace=True)
    bitcoin_df.drop(columns=['날짜'], inplace=True)

    # 볼린저 밴드 계산
    bitcoin_df = calculate_bollinger_bands(bitcoin_df)
    bitcoin_df.to_excel("bitcoin_df.xlsx")

def graphs():
    leaderboard_df = pd.read_excel("leaderboard_df.xlsx")
    bitcoin_df = pd.read_excel("bitcoin_df.xlsx")

    yesterday_open = bitcoin_df['Open'].iloc[-2]
    yesterday_close = bitcoin_df['Close'].iloc[-2]
    price_change = abs(yesterday_open - yesterday_close)

    # Bitcoin 종가 데이터를 사용하여 Plotly 그래프 생성
    fig = px.line(bitcoin_df, x='Date', y='Close')

    # 배경색 설정
    fig.update_layout(
        plot_bgcolor='#f3f6f4',  # 그래프 영역의 배경색
        paper_bgcolor='#f3f6f4'  # 그래프 영역 바깥의 배경색
    )

    fig.data[0].line.color = 'gray'  # 선 색상

    # mpi_df['Mpi_label'] 값이 -1인 날짜에 빨간색으로 X 표시 추가
    Mpi_points = []
    Whale_points = []
    Coinbase_points = []

    for index, row in bitcoin_df.iterrows():
        if row['Mpi_label'] == -1:
            Mpi_points.append(row['Date'])
        if row['Whale_label'] == -1:
            Whale_points.append(row['Date'])
        if row['Coinbase_label'] == -1:
            Coinbase_points.append(row['Date'])

    # 빨간점들을 하나의 trace로 추가
    fig.add_trace(
        go.Scatter(x=Mpi_points, y=bitcoin_df.loc[bitcoin_df['Date'].isin(Mpi_points), 'Close'].values, mode='markers',
                   marker=dict(symbol='x', color='#ffe03b', size=15),
                   text='Mpi', name='MPI'))

    fig.add_trace(
        go.Scatter(x=Whale_points, y=bitcoin_df.loc[bitcoin_df['Date'].isin(Whale_points), 'Close'].values, mode='markers',
                   marker=dict(symbol='x', color='#6ed93d', size=15),
                   text='Whale', name='Whale'))

    fig.add_trace(
        go.Scatter(x=Coinbase_points, y=bitcoin_df.loc[bitcoin_df['Date'].isin(Coinbase_points), 'Close'].values,
                   mode='markers',
                   marker=dict(symbol='x', color='#f78181', size=15),
                   text='Coinbase', name='Coinbase'))

    # BandWidth가 0.3 이상인 구간을 한 달 전부터 회색 배경색으로 추가
    for index, row in bitcoin_df.iterrows():
        if row['BandWidth'] >= 0.3:
            one_month_ago = row['Date'] - datetime.timedelta(days=5)
            fig.add_vrect(x0=one_month_ago, x1=row['Date'] + pd.DateOffset(1), fillcolor="gray", opacity=0.3,
                          layer="below", line_width=0)
    for index, row in leaderboard_df.iterrows():
        if row['예측 포지션'] == 'Long':
            # 초록색 가로줄 추가
            row['수익 (누적)'] = row['수익 (누적)'].replace(',', '')
            long_price = bitcoin_df.iloc[-1]['Close'] * (1 - float(row['수익 (일일)'])*(float(row['수익 (누적)'])/1000)/price_change)
            fig.add_hline(y=long_price, line_dash="dot", line_color="#6ed93d")
            # 라벨 추가
            fig.add_annotation(xref="paper", yref="y", x=1.02, y=long_price,
                               text=row['이름'], showarrow=False, font=dict(color="#6ed93d"))

        elif row['예측 포지션'] == 'Short':
            # 빨간 가로줄 추가
            row['수익 (누적)'] = row['수익 (누적)'].replace(',', '')
            short_price = bitcoin_df.iloc[-1]['Close'] * (1 + float(row['수익 (일일)'])*(float(row['수익 (누적)'])/1000)/price_change)
            fig.add_hline(y=short_price, line_dash="dot", line_color="#f78181")
            # 라벨 추가
            fig.add_annotation(xref="paper", yref="y", x=1.02, y=short_price,
                               text=row['이름'], showarrow=False, font=dict(color="#f78181"))

        # 그래프 레이아웃 설정
    fig.update_xaxes(title_text='날짜')
    fig.update_yaxes(title_text='종가')
    fig.update_layout(height=600)  # 원하는 높이로 설정

    # Streamlit 앱에 그래프 표시
    Chart.plotly_chart(fig, use_container_width=True)

def BTC_Price_update():
    binance = ccxt.binance()
    btc_data = binance.fetch_ohlcv("BTC/USDT", "1d", limit=1)

    btc_data = pd.DataFrame(btc_data)
    btc_data.to_excel("btc_data.xlsx")


def Summary():
    btc_data = pd.read_excel("btc_data.xlsx")

    # 현재 가격 및 등락률 업데이트
    BTC_Price = btc_data[4]
    BTC_Open = btc_data[1]
    BTC_Change = (BTC_Price - BTC_Open) * 100 / BTC_Open

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Pandas Series를 숫자로 변환
    BTC_Price_value = BTC_Price.item()
    BTC_Change_value = BTC_Change.item()

    with col1:
        BTC_Price_info.info('BTC Price', icon="📌")
        BTC_Price_placeholder.metric(label="BTC", value=f"{BTC_Price_value:,.0f} ({BTC_Change_value:.2f}%)")

    with col2:
        Time_info.info('Time', icon="📌")
        Time_placeholder.metric(label="Time", value=current_time)

def Indicator():
    mpi_df = pd.read_excel('채굴자 포지션 지표 (MPI).xlsx')
    Whale_df = pd.read_excel('거래소 고래 비율 (Exchange Whale Ratio).xlsx')
    Coinbase_df = pd.read_excel('코인베이스 프리미엄 지표.xlsx')

    mpi_filtered_df = mpi_df[mpi_df['label'] == -1]
    Whale_filtered_df = Whale_df[Whale_df['label'] == -1]
    Coinbase_filtered_df = Coinbase_df[Coinbase_df['label'] == -1]

    Indicator_info.info('Last Alert', icon="📌")
    Indicator1.metric(label="채굴자 포지션 지표(MPI)", value=f"{str(mpi_filtered_df['날짜'].dt.strftime('%Y-%m-%d').iloc[-1])} | {mpi_filtered_df['채굴자 포지션 지표 (MPI)'].iloc[-1]:.4f}")
    Indicator2.metric(label="거래소 고래 비율(Whale)", value=f"{str(Whale_filtered_df['날짜'].dt.strftime('%Y-%m-%d').iloc[-1])} | {Whale_filtered_df['거래소 고래 비율 (Exchange Whale Ratio)'].iloc[-1]:.4f}")
    Indicator3.metric(label="코인베이스 프리미엄 지표(Coinbase)", value=f"{str(Coinbase_filtered_df['날짜'].dt.strftime('%Y-%m-%d').iloc[-1])} | {Coinbase_filtered_df['코인베이스 프리미엄 지표'].iloc[-1]:.4f}")

def Leaderboard():
    df = pd.read_excel("leaderboard_df.xlsx", index_col=0)
    # df.drop(['Unnamed: 0'], axis=1, inplace=True)

    # 데이터프레임 출력
    Leaderboard_info.info('Leaderboard', icon="📌")
    Leaderboard1.dataframe(df)

# 1시간에 한번씩 graphs() 함수를 실행합니다.
last_run = datetime.datetime.now()

try:
    Summary()
except:
    pass
try:
    graphs()
except:
    pass
try:
    Indicator()
except:
    pass
try:
    Leaderboard()
except:
    pass

try:
    leaderbord_df_update()
    bitcoin_df_update()
    BTC_Price_update()
except:
    pass

try:
    Summary()
except:
    pass
try:
    graphs()
except:
    pass
try:
    Indicator()
except:
    pass
try:
    Leaderboard()
except:
    pass

while True:
    time.sleep(1)
    try:
        BTC_Price_update()
        Summary()
        # 현재 시간과 지난 시간 비교
        current_time = datetime.datetime.now()
        delta_time = current_time - last_run

        # 1시간이 지났으면 graphs() 함수를 실행합니다.
        if delta_time.total_seconds() > 3600:
            leaderbord_df_update()
            bitcoin_df_update()
            graphs()
            Indicator()
            Leaderboard()
            last_run = current_time
        # 1초마다 업데이트합니다.
    except:
        pass
#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""



