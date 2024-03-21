import pandas as pd
import os
from WebBrowser import seleniumGetData
import datetime
import numpy as np
from pandas_datareader import data
import pandas_datareader.data as web




# 取得絕對路徑，以便保存下載歷史資料
absPath = os.path.abspath("../")
historyDataPath = os.path.join(absPath, "data")

'''
ans = input('是否要下載歷史資料? (y/n)\n')
if ans.lower() == 'y':
    while True:
        stockName = input('請輸入股票名稱:\n')
        try:
            print("下載中...")
            seleniumGetData(historyDataPath, stockName)
            break
        except Exception as e:
            print(e)

while True:
    print('請選擇要讀取的資料:')
    csvList = os.listdir(historyDataPath)
    for index, csvFile in enumerate(csvList):
        print(f"{index}: {csvFile}")

    try:
        ans = int(input())
    except:
        print('輸入錯誤')
    if 0 <= ans < len(csvList):
        # 讀取並轉換為DataFrame
        df = pd.read_csv(os.path.join(historyDataPath, csvList[ans]))

        # 測試
        print(df.head())
        break
    else:
        print('輸入錯誤')
'''


os.system('pause')

