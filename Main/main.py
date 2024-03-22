import os
from API import StockManager

def main():
    # Get the absolute path and create a StockManager to manage downloaded historical data
    manager = StockManager(absPath=os.path.abspath("../"))

    while True:
        while True:
            print('Downloaded data:')
            manager.showStockList()
            ans = input('Select a stock from the list or choose another option. (A=Add New Stock, U=Update all History)\n')
            try:
                ans = int(ans)
                if 0 <= ans < len(manager.stockList):
                    index = ans
                    break
                else:
                    print("Input error")
            except:
                if ans.lower() == "a":
                    stockName = input("Please enter the stock name (Ex:2330.TW).\n")
                    manager.createStockClass(stockName)
                elif ans.lower() == "u":
                    manager.updateAll()
                else:
                    print("Input error")

        while True:
            ans = input("Select an action. (I=Show Company Info, H=Show History Data, U=Update History Data, 0=Return)\n")
            if ans.lower() == "i":
                manager.stockList[index].showCompanyInfo()
            elif ans.lower() == "h":
                manager.stockList[index].showHistoryData()
            elif ans.lower() == "u":
                manager.stockList[index].downloadHistoryData()
            elif ans == "0":
                break


main()
os.system('pause')
