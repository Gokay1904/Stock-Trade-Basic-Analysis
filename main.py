import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import datetime,time
import numpy as np
import re, requests
import json


symbols= ["IBM", "MSFT","TSLA", "XON"]
sharpe_ratios = {}
stocks = {}
_params = {
            "symbol":"Default",
            "apikey":"",
            "adjust":False,
            "function":"TIME_SERIES_DAILY"
}

def Add_And_Filter_Stocks():
    for s in symbols:
        _params["symbol"] = s

        response = requests.get("https://www.alphavantage.co/query?", params=_params)
        stock_df = response.json()
        print(stock_df)
        stock_with_time_and_close_price = {datetime.datetime.strptime(key, "%Y-%m-%d"): float(value["4. close"]) for (key, value) in stock_df['Time Series (Daily)'].items()}

        stocks[f"{s}"] = stock_with_time_and_close_price


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
        #print(f"day,{list(stock_dict.keys())[x]},{pct_change}")
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







#fig,ax  = plt.subplots(figsize = (10,4))
#
#ax.plot(current_stock.keys(),current_stock.values(),label="Closing Price")
#ax.plot(Day_7EMA["days"],Day_7EMA["ema"], label="7 DAY EMA")
#ax.plot(Day_30EMA["days"],Day_30EMA["ema"], label="30 DAY EMA")
#plt.ylabel('30-Date EMA')
#
#
#ax.set_title('TSLA Price Graph')
#
#plt.xlabel('Dates')
#plt.ylabel('Price')
#plt.legend()
#plt.xticks(rotation=90)


Add_And_Filter_Stocks()

#For Debugging
for s in symbols:
    current_stock = stocks[s]
    print(current_stock)

def Print_Shares(shares_dict):

    i = 0
    j = 0
    rowNum = 2
    colNum = 3

    fig, axs = plt.subplots(rowNum,colNum)

    plt.style.use('Solarize_Light2')


    for s in symbols:
       current_stock = shares_dict[s]

       #days = np.array(list(current_stock.keys()))

       sharpe = calculate_SHARPE(current_stock)
       print(f"Shape ratio for {s}: {calculate_SHARPE(current_stock)}")
       sharpe_ratios[s] = sharpe

       Day_7EMA = calculate_EMA(current_stock, 7)
       Day_30EMA = calculate_EMA(current_stock, 30)


       current_ax = axs[i,j]

       current_ax.set_title(f"{s} Closed Price Graph")

       current_ax.plot(current_stock.keys(),current_stock.values())
       #PLOT EMA's
       current_ax.plot(Day_7EMA["days"], Day_7EMA["ema"], label="7 DAY EMA")
       current_ax.plot(Day_30EMA["days"], Day_30EMA["ema"], label="30 DAY EMA")
       current_ax.text(3, 3, f'SHARPE RATIO: {sharpe}',fontsize = 20)
       current_ax.set_title(f"{s} Closed Price Graph")
       # PLOT Labels
       current_ax.set_ylabel('30-Date EMA')
       current_ax.set_xlabel('Dates')
       current_ax.set_ylabel('Price')

       # LEGEND
       current_ax.legend()

       plt.style.use('Solarize_Light2')

       # Rotate X 90 degree
       plt.xticks(rotation=90)

       # Next Iteration
       j = j+1

       if(j==colNum):
            j=0
            if(i <= rowNum-1):
                i = i+1


Print_Shares(stocks)


def Print_Sharpes(sharpe_dict):

    fig, ax = plt.subplots(figsize=(10, 4))
    plt.style.use('Solarize_Light2')

    ax.bar(sharpe_dict.keys(),sharpe_dict.values())
    plt.draw()
    plt.title("Sharpe Ratios for Stocks")
    plt.figtext(0,0,"<1 – Not good 1-1.99 – Ok 2-2.99 – Really good >3 – Exceptional",fontsize = 10)


Print_Sharpes(sharpe_ratios)


plt.show()







