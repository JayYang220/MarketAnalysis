import pandas as pd

# 讀取並轉換為DataFrame
df = pd.read_csv("../Data/BTC-USD.csv")

# 測試
print(df.head())