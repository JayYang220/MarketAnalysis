import yfinance as yf
import json
import requests
import pandas as pd
import numpy as np


class Stock():
    def __init__(self, stockName:str):
        self.stockName = stockName
        self.ticker = yf.Ticker(self.stockName)
        self.info = self.getInfo()

    def getInfo(self):
        return self.ticker.info

    def getHistory(self, period:str, interval:str):

        return yf.download(self.stockName, period='max', interval='1d')



# 測試用
if __name__ == '__main__':
    stock = Stock('2330.TW')
    print(stock.getHistory())



