#Imports
import datetime as dt
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import DateFormatter, date2num, WeekdayLocator, DayLocator, MONDAY


# insert here the start date and end date and then if you want put as arguments to data
start_date = '2022-11-20'
end_date = "2022-12-01" 

#insert here your currencies
tickers = ["AAPL","GOOG","AMZN"]


data = yf.download(tickers, start_date, end_date)
#data = yf.download(tickers, period = "1mo" , interval="1h", auto_adjust= True )

print(data)


"""
Graph area
"""


#moving average



data['Adj Close'].plot(figsize=(8,4))

plt.title("Adjusted Close Price of " + tickers[0] + " , " +  tickers[1] + " , " + tickers[2], fontsize=16)

plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)

plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)


plt.show()


"""

Create a candle graph

"""
tesla = yf.download("TSLA", start_date, end_date)

tesla_reset = tesla.loc['2021-01':'2021-01'].reset_index()

print(tesla_reset)

tesla_reset['date_ax'] = tesla_reset['Date'].apply(lambda date: date2num(date))

tesla_values = [tuple(vals) for vals in tesla_reset[['date_ax', 'Open', 'High', 'Low', 'Close']].values]

mondays = WeekdayLocator(MONDAY)

alldays = DayLocator()  

weekFormatter = DateFormatter('%b %d')

dayFormatter = DateFormatter('%d')


#Plot it
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)

candlestick_ohlc(ax, tesla_values, width=0.6,
colorup='g',colordown='r');
plt.show()
