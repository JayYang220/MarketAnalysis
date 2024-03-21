import yfinance as yf
import os
import pandas as pd

class StockManager:
    def __init__(self, absPath):
        self.historyDataPath = os.path.join(absPath, "Data")
        self.stockNameList = self.loadStockList()
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
        if stockName in self.stockNameList:
            return "股票名稱已存在"
        '''
        :param stockName:stockName
        :return: 成功時回傳Ture,否則False
        '''
        stock = Stock(self.historyDataPath, stockName)
        stock.getInfo()

        if stock.info is None:
            return "股票名稱錯誤或其他錯誤"
        else:
            stock.updateHistory()
            self.stockList.append(stock)
            self.stockNameList.append(stockName)
            return True

    def updateAll(self):
        for stock in self.stockList:
            stock.updateHistory()

    def showStockList(self):
        for index, stock in enumerate(self.stockNameList):
            print(f"{index:<3d} {stock}")

class Stock:
    def __init__(self, historyDataPath, stockName: str):
        self.stockName = stockName
        self.historyData = os.path.join(historyDataPath, self.stockName + ".csv")
        self.info = None
        self.history = None

    def showInfo(self):
        if self.info is None:
            self.getInfo()
        for key in self.info.keys():
            print(f"{key:30s} {self.info[key]}")

    def showHistoryData(self):
        if self.history is None:
            self.loadHistory()
        print(self.history.head)

    def getInfo(self) -> [dict, bool]:
        try:
            info = yf.Ticker(self.stockName).info
            if info["trailingPegRatio"] is not None:
                self.info = info
        except Exception as e:
            print(e)

    def updateHistory(self, period: str = "max", interval: str = '1d'):
        self.history = yf.download(self.stockName, period=period, interval=interval)
        self.history.to_csv(self.historyData)

    def loadHistory(self):
        try:
            self.history = pd.read_csv(self.historyData)
        except Exception as e:
            print(e)

# 測試用
if __name__ == '__main__':
    info = {'trailingPegRatio': '1.5'}
    print(info["trailingPegRatio"] is None)