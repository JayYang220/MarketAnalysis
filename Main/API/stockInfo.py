import yfinance as yf
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

    def createStockClass(self, stockName: str) -> [bool]:
        """
        :param stockName:stockName
        :return: 成功時回傳Ture,否則False
        """
        if stockName in self.stockNameList:
            raise "股票已存在"

        # 嘗試downloadCompanyInfo，判斷股票名稱使否存在
        try:
            stock = Stock(self.historyDataPath, stockName)
            stock.downloadCompanyInfo()
        except Exception as e:
            print(e)
            return

        self.stockList.append(stock)
        self.stockNameList.append(stockName)
        print(f"{stock} 加入成功")


    def updateAll(self):
        """更新所有股票資訊"""
        for stock in self.stockList:
            stock.downloadHistoryData()

    def showStockList(self):
        """顯示庫存的CSV名稱"""
        for index, stock in enumerate(self.stockNameList):
            print(f"{index:<3d} {stock}")

class Stock:
    def __init__(self, historyDataPath, stockName: str):
        self.stockName = stockName
        self.historyDataFile = os.path.join(historyDataPath, self.stockName + ".csv")

        # 公司資訊及歷史股價初始化為None，待使用者輸入需求時再抓取
        self.companyInfo = None
        self.historyData = None

    def showCompanyInfo(self):
        """顯示 CompanyInfo"""
        if self.companyInfo is None:
            self.downloadCompanyInfo()
        for key in self.companyInfo.keys():
            print(f"{key:30s} {self.companyInfo[key]}")

    def downloadCompanyInfo(self):
        """Download CompanyInfo"""
        info = yf.Ticker(self.stockName).info
        # 不確定為什麼stockName不存在時，仍會回傳dict，使用下面的特徵來判定是否成功
        if info["trailingPegRatio"] is not None:
            self.companyInfo = info
        else:
            raise AssertionError("股票名稱錯誤或其他錯誤")

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

    def downloadHistoryData(self, period: str = "max", interval: str = '1d'):
        """Download HistoryData"""
        # 舊方法
        # yf.pdr_override()
        # start_date = dt.datetime(1900, 1, 10)
        # end_date = dt.datetime(2100, 3, 18)
        # self.history = web.get_data_yahoo(self.stockName, start_date, end_date)

        self.historyData = yf.download(self.stockName, period=period, interval=interval)
        self.historyData.to_csv(self.historyDataFile)
        print(f"{self.stockName:10s} 更新完成")


