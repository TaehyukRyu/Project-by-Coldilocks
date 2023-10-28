from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import subprocess
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import traceback
#파일읽어오기
import pandas as pd
import numpy as np
import seaborn as sns
import warnings
from sklearn.cluster import DBSCAN
import telegram, asyncio
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import matplotlib

def Crawling():
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

    url = "https://cryptoquant.com/ko/asset/btc/chart/flow-indicator/miners-position-index-mpi?window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line"
    key_word = '채굴자 포지션 지표 (MPI)'

    option = Options()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',}
    option.add_argument(f"--headers={headers}")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()
    driver.get(url)

    time.sleep(6)

    # 대상 텍스트의 위치
    start_x, start_y = 370, 700
    end_x, end_y = 1822, 700

    # start_x, start_y = 1810, 700
    # end_x, end_y = 1819, 700

    df = pd.DataFrame(columns=["날짜", "가격", f"{key_word}"])
    previous_date = ""

    pyautogui.moveTo(2000, 700)
    n=0
    # 마우스 이동 루프
    for x in range(start_x, end_x + 1):
        try:
            # 마우스 이동
            pyautogui.moveTo(x, start_y)
            time.sleep(0.001)  # 이동 시간을 위해 적절한 대기 시간을 설정할 수 있습니다.

            # 텍스트 요소 추출
            element = driver.find_element(By.CSS_SELECTOR, 'body > div.highcharts-tooltip-container > svg > g > text')
            text_value = element.text
            # print("텍스트 값:", text_value)


            # 텍스트 분석 및 데이터 추출
            parts = text_value.split("●")
            date = parts[0].strip()
            price = parts[1].split("◆")[0].strip().replace("가격(USD):", "")
            cdd = parts[1].split("◆")[1].strip().replace(f"{key_word}:", "")
            print(date)

            print(cdd)

            # print("날짜:", date)
            # print("가격:", price)
            # print("CDD:", cdd)

            # 이전 날짜와 현재 날짜를 비교하여 다를 경우에만 저장
            if date != previous_date:
                # 데이터를 데이터 프레임에 추가
                new_data = pd.DataFrame({"날짜": [date], "가격": [price], f"{key_word}": [cdd]})
                df = pd.concat([df, new_data], ignore_index=True)
                # 현재 날짜를 이전 날짜로 업데이트
                previous_date = date

        except Exception as e:
            # 오류 메시지 출력
            print(f"오류 발생: {e}")
            traceback.print_exc()  # 상세한 오류 트레이스백 출력
            # print(n)
            print("n: ", n)
            n+=1

    # 데이터 프레임을 Excel 파일로 저장
    print("n: ",n)
    df.to_excel(f'{key_word}.xlsx', index=False)


    #####################################################################################################

    url = "https://cryptoquant.com/ko/asset/btc/chart/market-data/coinbase-premium-gap?window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line"
    key_word = '코인베이스 프리미엄 지표'

    option = Options()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',}
    option.add_argument(f"--headers={headers}")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()
    driver.get(url)

    time.sleep(6)

    # 대상 텍스트의 위치
    start_x, start_y = 370, 700
    end_x, end_y = 1822, 700

    # start_x, start_y = 1810, 700
    # end_x, end_y = 1819, 700

    df = pd.DataFrame(columns=["날짜", "가격", f"{key_word}"])
    previous_date = ""

    pyautogui.moveTo(2000, 700)
    n=0
    # 마우스 이동 루프
    for x in range(start_x, end_x + 1):
        try:
            # 마우스 이동
            pyautogui.moveTo(x, start_y)
            time.sleep(0.001)  # 이동 시간을 위해 적절한 대기 시간을 설정할 수 있습니다.

            # 텍스트 요소 추출
            element = driver.find_element(By.CSS_SELECTOR, 'body > div.highcharts-tooltip-container > svg > g > text')
            text_value = element.text
            # print("텍스트 값:", text_value)


            # 텍스트 분석 및 데이터 추출
            parts = text_value.split("●")
            date = parts[0].strip()
            price = parts[1].split("◆")[0].strip().replace("가격(USD):", "")
            cdd = parts[1].split("◆")[1].strip().replace(f"{key_word}:", "")
            print(date)

            print(cdd)

            # print("날짜:", date)
            # print("가격:", price)
            # print("CDD:", cdd)

            # 이전 날짜와 현재 날짜를 비교하여 다를 경우에만 저장
            if date != previous_date:
                # 데이터를 데이터 프레임에 추가
                new_data = pd.DataFrame({"날짜": [date], "가격": [price], f"{key_word}": [cdd]})
                df = pd.concat([df, new_data], ignore_index=True)
                # 현재 날짜를 이전 날짜로 업데이트
                previous_date = date

        except Exception as e:
            # 오류 메시지 출력
            print(f"오류 발생: {e}")
            traceback.print_exc()  # 상세한 오류 트레이스백 출력
            # print(n)
            print("n: ", n)
            n+=1

    # 데이터 프레임을 Excel 파일로 저장
    print("n: ",n)
    df.to_excel(f'{key_word}.xlsx', index=False)

    #####################################################################################################

    url = "https://cryptoquant.com/ko/asset/btc/chart/flow-indicator/exchange-whale-ratio?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line"
    key_word = '거래소 고래 비율 (Exchange Whale Ratio)'

    option = Options()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',}
    option.add_argument(f"--headers={headers}")
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()
    driver.get(url)

    time.sleep(6)

    # 대상 텍스트의 위치
    start_x, start_y = 370, 700
    end_x, end_y = 1822, 700

    # start_x, start_y = 1810, 700
    # end_x, end_y = 1819, 700

    df = pd.DataFrame(columns=["날짜", "가격", f"{key_word}"])
    previous_date = ""

    pyautogui.moveTo(2000, 700)
    n=0
    # 마우스 이동 루프
    for x in range(start_x, end_x + 1):
        try:
            # 마우스 이동
            pyautogui.moveTo(x, start_y)
            time.sleep(0.001)  # 이동 시간을 위해 적절한 대기 시간을 설정할 수 있습니다.

            # 텍스트 요소 추출
            element = driver.find_element(By.CSS_SELECTOR, 'body > div.highcharts-tooltip-container > svg > g > text')
            text_value = element.text
            # print("텍스트 값:", text_value)


            # 텍스트 분석 및 데이터 추출
            parts = text_value.split("●")
            date = parts[0].strip()
            price = parts[1].split("◆")[0].strip().replace("가격(USD):", "")
            cdd = parts[1].split("◆")[1].strip().replace(f"{key_word}:", "")
            print(date)

            print(cdd)

            # print("날짜:", date)
            # print("가격:", price)
            # print("CDD:", cdd)

            # 이전 날짜와 현재 날짜를 비교하여 다를 경우에만 저장
            if date != previous_date:
                # 데이터를 데이터 프레임에 추가
                new_data = pd.DataFrame({"날짜": [date], "가격": [price], f"{key_word}": [cdd]})
                df = pd.concat([df, new_data], ignore_index=True)
                # 현재 날짜를 이전 날짜로 업데이트
                previous_date = date

        except Exception as e:
            # 오류 메시지 출력
            print(f"오류 발생: {e}")
            traceback.print_exc()  # 상세한 오류 트레이스백 출력
            # print(n)
            print("n: ", n)
            n+=1

    # 데이터 프레임을 Excel 파일로 저장
    print("n: ",n)
    df.to_excel(f'{key_word}.xlsx', index=False)

def Alert():
    matplotlib.use('TkAgg')

    warnings.filterwarnings("ignore")
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    sns.set_context('talk')

    tel_token = '6681190218:AAFjkYadBFWELgJ12zwmAdyvYUFZXTgo7_k'
    chat_id = '-1001576547310'
    bot = telegram.Bot(token=tel_token)

    mpi_df = pd.read_excel('채굴자 포지션 지표 (MPI).xlsx')

    try:
        #변수형식설정
        mpi_df['날짜'] = pd.to_datetime(mpi_df['날짜'], format = "%Y %m %d")
        mpi_df['가격'] = mpi_df['가격'].str.replace(',', '').astype(float)
        mpi_df['가격'] = pd.to_numeric(mpi_df['가격'], errors='coerce')
    except:
        pass


    #스케일링(정규화)
    scaler = MinMaxScaler()
    mpi_df[['scaled_MPI']] = scaler.fit_transform(mpi_df[['채굴자 포지션 지표 (MPI)']])

    X = mpi_df[['scaled_MPI']].values
    dbscan = DBSCAN(eps=0.03, min_samples=12).fit(X)
    labels = dbscan.labels_

    #label컬럼 추가
    mpi_df['label'] = labels

    # 마지막 데이터의 label 값 확인
    mpi_last_label = mpi_df.iloc[-1]['label']

    # -1인 경우 메시지 전송
    if mpi_last_label == -1:
        # 텔레그램 봇 초기화
        bot = telegram.Bot(token=tel_token)

        # 메시지 전송
        message = "채굴자 포지션 지표 (MPI)에서 이상치가 감지되었습니다."
        asyncio.run(bot.sendMessage(chat_id, message))

    mpi_df.to_excel('채굴자 포지션 지표 (MPI).xlsx', index=False)

    ##################################################################################


    Whale_df = pd.read_excel('거래소 고래 비율 (Exchange Whale Ratio).xlsx')

    try:
        #변수형식설정
        Whale_df['날짜'] = pd.to_datetime(Whale_df['날짜'], format = "%Y %m %d")
        Whale_df['가격'] = Whale_df['가격'].str.replace(',', '').astype(float)
        Whale_df['가격'] = pd.to_numeric(Whale_df['가격'], errors='coerce')
    except:
        pass

    #스케일링(정규화)
    scaler = MinMaxScaler()
    Whale_df[['scaled_EWR']] = scaler.fit_transform(Whale_df[['거래소 고래 비율 (Exchange Whale Ratio)']])

    X = Whale_df[['scaled_EWR']].values
    dbscan = DBSCAN(eps=0.04, min_samples=12).fit(X)
    labels = dbscan.labels_

    #label컬럼 추가
    Whale_df['label'] = labels

    bot = telegram.Bot(token=tel_token)

    # 마지막 데이터의 label 값 확인
    Whale_last_label = Whale_df.iloc[-1]['label']

    # -1인 경우 메시지 전송
    if Whale_last_label == -1:
        # 텔레그램 봇 초기화
        bot = telegram.Bot(token=tel_token)

        # 메시지 전송
        message = "거래소 고래 비율 (Exchange Whale Ratio)에서 이상치가 감지되었습니다."
        asyncio.run(bot.sendMessage(chat_id, message))

    Whale_df.to_excel('거래소 고래 비율 (Exchange Whale Ratio).xlsx', index=False)

    ####################################################################################
    Coinbase_df = pd.read_excel('코인베이스 프리미엄 지표.xlsx')

    try:
        Coinbase_df['날짜'] = pd.to_datetime(Coinbase_df['날짜'])
        Coinbase_df['가격'] = Coinbase_df['가격'].str.replace(',', '').astype(float)
    except:
        pass

    scaler = MinMaxScaler()
    Coinbase_df[['코인베이스 프리미엄 지표']] = scaler.fit_transform(Coinbase_df[['코인베이스 프리미엄 지표']])

    model = DBSCAN(eps=0.01, min_samples=10).fit(X)  # contamination 파라미터는 이상치의 비율을 설정합니다.
    labels = dbscan.labels_

    # label컬럼 추가
    Coinbase_df['label'] = labels

    bot = telegram.Bot(token=tel_token)

    # 마지막 데이터의 label 값 확인
    Coinbase_last_label = Coinbase_df.iloc[-1]['label']

    # -1인 경우 메시지 전송
    if Coinbase_last_label == -1:
        # 텔레그램 봇 초기화
        bot = telegram.Bot(token=tel_token)

        # 메시지 전송
        message = "코인베이스 프리미엄 지표에서 이상치가 감지되었습니다."
        asyncio.run(bot.sendMessage(chat_id, message))

    Coinbase_df.to_excel('코인베이스 프리미엄 지표.xlsx', index=False)

while True:
    Crawling()
    Alert()
    time.sleep(21600)