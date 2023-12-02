import pandas as pd
from matplotlib import pyplot as plt
import yfinance as yf

class Patterns():
    def __init__(self,excel):
        #read the excel info
        self.df = pd.read_csv(excel)
        self.conv = " ";
        self.info = {} #save the data
        self.BearOrBull = {} #define for each candle if it is a bull or bear candle (BULL or BEAR)
        self.inter = {} #save the interpolation functions
        self.inter_mean = {} #save the interpolation functions of the mean between open and close
        self.marks = {} #save all possible resistences and suports 
        self.trends = {"UP" : [], "DOWN" : []} # for exemple: {"DOWN" : [[3,7],[15,25]] , "UP" : [[70,80]]}

    def convert(self):
        self.conv = self.df.to_string()
        end_line_index = 114


        for ii in range(0,len(self.conv)//114):
                
            #indexs
            open_index = [end_line_index+32,end_line_index+33+10]
            high_index = [open_index[1],open_index[1]+12]
            low_index = [high_index[1],high_index[1]+12]
            close_index = [low_index[1],low_index[1]+12]
            volume_index = [close_index[1],close_index[1]+10]

            #values of the dictionary
            open = self.conv[open_index[0]:open_index[1]]
            high = self.conv[high_index[0]:high_index[1]]
            low = self.conv[low_index[0]:low_index[1]]
            close = self.conv[close_index[0]:close_index[1]]
            volume =  self.conv[volume_index[0]:volume_index[1]]

            #adding info to the dictionary
            self.info[ii] = [float(open),float(high),float(low),float(close),float(volume)] 

            #changing the indexs        
            end_line_index += 114
    def BearishoOrBullish(self): #red or green candle
        for ii in range(0,len(self.conv)//114):
            if self.info[ii][0] < self.info[ii][3]:
                self.BearOrBull[ii] = "BULL"
            else:
                self.BearOrBull[ii] = "BEAR"
                
    def Interpolation(self):

        for ii in range(0,len(self.conv)//114-1):
            open1 = self.info[ii][0]
            high1 = self.info[ii][1]
            low1 = self.info[ii][2]
            close1 = self.info[ii][3]
            volume1 = self.info[ii][4]

            open2 = self.info[ii+1][0]
            high2 = self.info[ii+1][1]
            low2 = self.info[ii+1][2]
            close2 = self.info[ii+1][3]
            volume2 = self.info[ii+1][4]

            m_open = open2 - open1
            m_high = high2 - high1
            m_low = low2 - low1
            m_close = close2 - close1
            m_volume = volume2 - volume1

            self.inter[ii] = [m_open,m_high,m_low,m_close,m_volume]

            mean1 = (open1 + close1)/2
            mean2 = (open2 + close2)/2

            m_mean = mean2 - mean1

            self.inter_mean[ii] = m_mean
    

    def Marks(self):
        positive_m = True 
        for ii in range(0,len(self.conv)//114-1):
            if ii == 0: 
                if self.inter_mean[ii] < 0: 
                    positive_m = False
                else:
                    positive_m = True
            else:
                if positive_m == True and self.inter_mean[ii] < 0: #In this case I want the higher value
                    if self.info[ii][0] > self.info[ii][1]:     
                        self.marks[ii] = self.info [ii][0]
                    if self.info[ii][0] < self.info[ii][1]:     
                        self.marks[ii] = self.info [ii][1]
                    positive_m = False
                if positive_m == False and self.inter_mean[ii] > 0: #In this case I want the lower value
                    if self.info[ii][0] < self.info[ii][1]:     
                        self.marks[ii] = self.info [ii][0]
                    if self.info[ii][0] > self.info[ii][1]:     
                        self.marks[ii] = self.info [ii][1]
                    positive_m = True        

            
    def Checker(self,interval1,interval2):
        
        if abs(interval2 - interval1) < 4:
            print("Error in function Cheker (Line 106) : Interval2 - Interval1 must be bigger then 4.")
            return 0
        
        keys = sorted(self.marks.keys())[interval1:interval2+1]
        
        down_trend = True
        up_trend = True

        values_ii_pares = []
        values_ii_impares = []
        for ii in range(0,len(keys)):
            if ii % 2 == 0:
                values_ii_pares.append(ii)
            if ii % 2 == 1:
                values_ii_impares.append(ii)

        for ii in range(0,len(values_ii_pares)-1):
            if self.marks[keys[values_ii_pares[ii+1]]] - self.marks[keys[values_ii_pares[ii]]] <= 0:
                up_trend = False

            if self.marks[keys[values_ii_pares[ii+1]]] - self.marks[keys[values_ii_pares[ii]]] >= 0:
                down_trend = False

        for ii in range(0,len(values_ii_impares)-1):
            if self.marks[keys[values_ii_impares[ii+1]]]-self.marks[keys[values_ii_impares[ii]]] <= 0:
                up_trend = False

            if self.marks[keys[values_ii_impares[ii+1]]] - self.marks[keys[values_ii_impares[ii]]] >= 0:
                down_trend = False


        if down_trend == True:
            return [True,"down"]
        if up_trend == True:
            return [True,"up"]
        else:
            return [False,"None"]

    def Down_Up_Trends(self):


        #keys of marks  

        keys = sorted(self.marks.keys()) 


        # here I will store EVERY trends,
        # including trends inside trends
        # (ex: there are a down trend between [0,10]
        # and there are also a down trend between [0,12],
        # this list will store both) -> of course then I
        # are going to filter this list in order to just
        # consider the bigger one

        lista_Down = []
        lista_Up = [] 



        for ii in range(0,len(keys)-4):
            for jj in range(4,len(keys)):
                try:
                    A = self.Checker(interval1 = ii,interval2 = ii+jj)
                except:
                    break
                if A[0] == True:
                    if A[1] == "down":
                        try:
                            lista_Down.append([keys[ii],keys[ii+jj]])
                        except:
                            break
                    if A[1] == "up":
                        try:
                            lista_Up.append([keys[ii],keys[ii+jj]])
                        except:
                            break            
                if A[0] == False:
                    break



        


    def print(self):

        print("------------- MARKS -----------------")
        print(self.marks)
        print("------------------------------------")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
"""
        print("------------- INFO -----------------")
        print(self.info)
        print("------------------------------------")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("------------- INTER -----------------")
        print(self.inter)
        print("------------------------------------")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")

        print("------------- BEAR AND BULL -----------------")
        print(self.BearOrBull)
        print("------------------------------------")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")

        print("------------- DOWNUPTREND -----------------")
        print(self.trends)
        print("------------------------------------")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
"""





    