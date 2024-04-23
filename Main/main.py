import os
from API import StockManager

debug = False
__version__ = "1.2.0"

def main():
    # Get the absolute path and create a StockManager to manage downloaded historical data
    manager = StockManager(abs_path=os.path.abspath("../"))

    while True:
        while True:
            print('Downloaded data:')
            manager.show_stock_list()
            if debug:
                ans = '0'
            else:
                ans = input('Select a stock from the list or choose another option. (A=Add New Stock, U=Update all History)\n')

            try:
                ans = int(ans)
                if 0 <= ans < len(manager.stock_class_list):
                    index = ans
                    break
                else:
                    print("Input error")

            except ValueError:
                if ans.lower() == "a":
                    stock_name = input("Please enter the stock name (Ex:2330.TW).\n")
                    manager.create_stock_class(stock_name)
                elif ans.lower() == "u":
                    manager.update_all()
                else:
                    print("Input error")

            except Exception as e:
                print(f"Unknow Error: {e}")

        while True:
            if debug:
                ans = 'a'
            else:
                ans = input("Select an action. (I=Show Company Info, H=Show History Data, U=Update History Data, L=LTSM Function, 0=Return)\n")
            if ans.lower() == "i":
                # Show Company Info
                manager.stock_class_list[index].show_company_info()
            elif ans.lower() == "h":
                # Show History Data
                manager.stock_class_list[index].show_history_data()
            elif ans.lower() == "u":
                # Update History Data
                manager.stock_class_list[index].download_history_data()
            elif ans.lower() == "l":
                # LTSM Function
                manager.stock_class_list[index].LSTM_function()
            elif ans == "0":
                break
            if debug:
                os.system('pause')

if __name__ == "__main__":
    main()
    os.system('pause')
