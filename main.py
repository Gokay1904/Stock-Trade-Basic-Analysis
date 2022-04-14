import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as pt
import datetime,time
import numpy as np
import re, requests
import json


symbols= ["IBM", "MSFT", "APPL"]


_params = {
            "symbol":"AAPL",
            "apikey":"VIIFUUVM2CJN6WRL",
            "adjust":False,
            "function":"TIME_SERIES_DAILY"
}

response = requests.get("https://www.alphavantage.co/query?",params = _params)


stock_df = response.json()


combined_dict = {datetime.datetime.strptime(key, "%Y-%m-%d"): float(value["4. close"]) for (key,value) in stock_df['Time Series (Daily)'].items()}
days = np.array(list(combined_dict.keys()))

def calculate_SHARPE(stock_dict,risk_free_rate = 0):
    '''<1 – Not good
        1-1.99 – Ok
        2-2.99 – Really good
        >3 – Exceptional'''
    std = percentage_change(stock_dict).std()

    avrg = percentage_change(stock_dict).mean()

    return (((avrg - risk_free_rate)/std) *(252**0.5))

#DUZENLENECEK
def percentage_change(stock_dict):

    prices = np.array(list(stock_dict.values()))
    pct_change_array = np.zeros(len(prices))
    for x in range(0,len(prices)-1):
        pct_change = ((prices[x] - prices[x+1])/prices[x] * 100)
        print(f"day,{list(stock_dict.keys())[x]},{pct_change}")
        pct_change_array[x] = pct_change


    return pct_change_array[0:pct_change_array.size-1]


def calculate_EMA(stock_dict,days, smoothing = 2):

    prices = np.array(list(stock_dict.values()))
    days_list = list(stock_dict.keys())
    days_list = days_list[0:len(days_list)-(days-1)]


    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1+ days))) + (ema[-1] * (1-(smoothing / (1+days)))))


    ema_by_days = { "ema" : ema,"days": days_list}

    return ema_by_days



print(calculate_SHARPE(combined_dict))
Day_7EMA = calculate_EMA(combined_dict,7)
Day_30EMA = calculate_EMA(combined_dict,30)


fig, ax = plt.subplots(figsize = (10,4))

ax.plot(combined_dict.keys(),combined_dict.values(),label="Closing Price")
ax.plot(Day_7EMA["days"],Day_7EMA["ema"], label="7 DAY EMA")
ax.plot(Day_30EMA["days"],Day_30EMA["ema"], label="30 DAY EMA")
plt.ylabel('30-Date EMA')


ax.set_title('TSLA Price Graph')

plt.xlabel('Dates')
plt.ylabel('Price')
plt.legend()
plt.xticks(rotation=90)

plt.show()






