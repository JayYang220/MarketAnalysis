import pandas as pd
import os
from API import StockManager


def main():
    # 取得絕對路徑及建立StockManager，管理下載的歷史資料
    manager = StockManager(absPath=os.path.abspath("../"))

    while True:
        while True:
            print('已下載的資料:')
            manager.showStockList()
            ans = input('選擇股票或其他功能 (A=Add New Stock, U=Update all History)\n')
            try:
                ans = int(ans)
                if 0 <= ans < len(manager.stockList):
                    index = ans
                    break
            except:
                if ans.lower() == "a":
                    stockName = input("請輸入股票名稱:\n")
                    res = manager.createStockClass(stockName)
                    if res is not True:
                        print(res)

                elif ans.lower() == "u":
                    manager.updateAll()
                else:
                    print("輸入錯誤")

        while True:
            ans = input("選擇功能 (I=Show Company Info, H=Show History Data, U=UpdateHistoryData, 0=Return)\n")
            if ans.lower() == "i":
                manager.stockList[index].showInfo()
            elif ans.lower() == "h":
                manager.stockList[index].showHistoryData()
            elif ans.lower() == "u":
                manager.stockList[index].updateHistory()
            elif ans == "0":
                break


main()

os.system('pause')
