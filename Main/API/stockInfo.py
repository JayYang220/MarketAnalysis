import yfinance as yf
# Guide https://pypi.org/project/yfinance/
# Guide https://algotrading101.com/learn/yahoo-finance-api-guide/
import os
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime as dt

class StockManager:
    def __init__(self, absPath):
        self.historyDataPath = os.path.join(absPath, "Data")

        # 讀取庫存的CSV名稱 集中成list管理
        self.stockNameList = self.loadStockList()

        # 建立stock class 集中成list管理
        self.stockList = self.initStockClass()

    def loadStockList(self):
        if os.path.exists(self.historyDataPath) is False:
            os.mkdir(self.historyDataPath)
            return []
        else:
            fileList = os.listdir(self.historyDataPath)
            fileListWithoutExtension = [os.path.splitext(file)[0] if file.endswith('.csv') else file for file in fileList]
            self.stockNameList = fileListWithoutExtension
            return fileListWithoutExtension

    def initStockClass(self):
        stockClassList = []
        for stockName in self.stockNameList:
            stockClassList.append(Stock(self.historyDataPath, stockName))
        return stockClassList

    def createStockClass(self, stockName: str):
        if stockName in self.stockNameList:
            print("This stock already exists in the list.")
            return

        # 嘗試downloadTicker，若名稱不存在時會拋出錯誤
        try:
            stock = Stock(self.historyDataPath, stockName)
            stock.downloadTicker()
            stock.downloadHistoryData()
        except Exception as e:
            print(e)
            print("You can retrieve stock names from Yahoo Finance at https://finance.yahoo.com/")
            return

        self.stockList.append(stock)
        self.stockNameList.append(stockName)
        print(f"{stockName} Addition completed")


    def updateAll(self):
        """更新所有股票資訊"""
        for stock in self.stockList:
            stock.downloadHistoryData()

    def showStockList(self):
        """顯示庫存的CSV名稱"""
        for index, stock in enumerate(self.stockNameList):
            print(f"{index:>3d}. {stock}")

class Stock:
    def __init__(self, historyDataPath, stockName: str):
        self.stockName = stockName
        self.historyDataFile = os.path.join(historyDataPath, self.stockName + ".csv")

        # 初始化為None，待使用者輸入需求時再抓取
        self.ticker = None
        self.companyInfo = None
        self.historyData = None

    def downloadTicker(self):
        """下載 ticker"""
        self.ticker = yf.Ticker(self.stockName)
        self.companyInfo = self.ticker.info

        # 股票名稱錯誤時，仍會返回一個dict，利用下列特徵確認股票名稱是否正確
        if 'previousClose' not in self.ticker.info:
            raise AssertionError("Stock name error.")
        self.historyData = self.ticker.history(period='max', interval='1d')

    def showCompanyInfo(self):
        """顯示 CompanyInfo"""
        if self.ticker is None:
            self.downloadTicker()
        for key in self.companyInfo.keys():
            print(f"{key:30s} {self.companyInfo[key]}")

    def showHistoryData(self):
        """顯示 HistoryData"""
        if self.historyData is None:
            self.loadHistory()
        print(self.historyData.head)

    def loadHistory(self):
        """讀取 HistoryData"""
        try:
            self.historyData = pd.read_csv(self.historyDataFile)
        except Exception as e:
            print(e)

    def downloadHistoryData(self, period: str = 'max', interval: str = '1d'):
        """Download HistoryData"""
        # 舊方法
        # yf.pdr_override()
        # start_date = dt.datetime(1900, 1, 10)
        # end_date = dt.datetime(2100, 3, 18)
        # self.history = web.get_data_yahoo(self.stockName, start_date, end_date)

        self.downloadTicker()
        self.historyData.to_csv(self.historyDataFile)
        print(f"{self.stockName} Update completed")

# 測試用
if __name__ == "__main__":
    stockName = "2330.TW"
    ticker = yf.Ticker(stockName)
    print(ticker.info)
