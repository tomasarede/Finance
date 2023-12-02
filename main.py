from ReadMarket import *
from Patterns import *


"""
READING THE MARKET AND GETTING INFO
"""

#Create the var market
market = ReadMarket()

#Choose the currency
market.choose_currency()

#Choose the time frame of the graph (last x days ; time frame of y time)
market.choose_period_interval('30d','1h')

#Create the excel with info of the market
market.create_excel()

#Read the excel created
market.read_excel()

#Ask if wanna see graphs (If you don't want you can just comment the line above with #)
market.ask_graphs()

"""
ANALYSING THE PATTERNS 
"""

a = Patterns("TSLA_Data.csv")
a.convert()
a.BearishoOrBullish()
a.Interpolation()
a.Marks()
a.Down_Up_Trends()
a.print()
