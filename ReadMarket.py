import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as pl
import yfinance as yf

class ReadMarket():

    def __init__(self):
        self.stocks = 0
        self.df = 0

    def choose_currency(self):
        print("""\
    _____ _                             _____                                     
    / ____| |                           / ____|                                    
    | |    | |__   ___   ___  ___  ___  | |    _   _ _ __ _ __ ___ _ __   ___ _   _ 
    | |    | '_ \ / _ \ / _ \/ __|/ _ \ | |   | | | | '__| '__/ _ \ '_ \ / __| | | |
    | |____| | | | (_) | (_) \__ \  __/ | |___| |_| | |  | | |  __/ | | | (__| |_| |
    \_____|_| |_|\___/ \___/|___/\___|  \_____\__,_|_|  |_|  \___|_| |_|\___|\__, |
                                                                            __/ |
                                                                            |___/ 
            """)
        name_of_currency = str(input('Name of currency: ')).strip().upper()
        self.stocks = yf.Ticker(name_of_currency)


    #2º Step: Choose the period and interval you want to work with
    def choose_period_interval(self,per,inter):
        self.df = self.stocks.history(period = per, interval= inter)


    #3º Step: Transfer data for csv file
    def create_excel(self):
        self.df.to_csv("TSLA_Data.csv")

    #4º Step: Read the data of csv file
    def read_excel(self):
        self.df = pd.read_csv("TSLA_Data.csv")


    #5º Step: Make graphs if wanted

    
    def candlestick_graph(self):
        candlestick = pl.Candlestick(x = self.df.index,
                                    low = self.df['Low'],
                                    high = self.df['High'],
                                    close = self.df['Close'],
                                    open = self.df['Open'])
        fig = pl.Figure(data=[candlestick])
        fig.show()

    def normal_graph(self):
        self.df['Close'].plot(figsize=(8,4))
        plt.ylabel('Price', fontsize=14)
        plt.xlabel('Date', fontsize=14)
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()
        

    def ask_graphs(self):
        print(""" \
        
    _____                 _         
    / ____|               | |        
    | |  __ _ __ __ _ _ __ | |__  ___ 
    | | |_ | '__/ _` | '_ \| '_ \/ __|
    | |__| | | | (_| | |_) | | | \__ _
    \_____|_|  \__,_| .__/|_| |_|___/
                    | |              
                    |_|              
    
        """)

        answer = str(input('Wanna see a candlestick graph (S/N) ?  ')).strip().upper()

        if answer == "S" :
            self.candlestick_graph()

        answer2 = str(input('Wanna see a normal graph with close prices (S/N) ?  ')).strip().upper()

        if answer2 == "S":
            self.normal_graph()




    


