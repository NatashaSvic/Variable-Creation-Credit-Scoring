# Import Libraries

import pandas as pd
import pandas_datareader.data as web
import datetime
import time
from random import randint

#Read the File
df_g = pd.read_excel("GOOG_Financials13-17.xlsx")
df_g.head()

'''Variable Creation'''

#Average Total Asset
df_g['Avg_Total_Asset'] = df_g['Total Assets']/len(df_g)
#Creating Current Ratio (Liquidity)
df_g['Current Ratio'] = df_g['Current Assets']/df_g['Current Liabilities']
#Creating Debt to Equity Ratio (Solvency)
df_g['Debt to Equity Ratio'] = df_g['Total Liabilities']/df_g['Total Shareholder Equity']
#Creating Return on Assets
df_g['ROA'] = df_g['Net Income']/df_g['Avg_Total_Asset']
#Creating Return on Assets
df_g['Asset Turnover Ratio'] = df_g['Sales']/df_g['Avg_Total_Asset']
df_g.head()

'''External Variables'''
#Obtaining past 5 years data of stock information of Google from Yahoo using datareader
def safe_read_yahoo_finance(stock):
    ''' Function for safe requesting information from Yahoo Finance Key Statistics for a given stock. 
    If Yahoo fails to respond, it sleeps for random number of second between 1 to 12 seconds and then try again.
    The functions tries again up to 10 times! '''
    df_stock = ''
    ntries = 0
    while (df_stock == '') and (ntries < 10):
        try:
            edate =   datetime.datetime.now()
            sdate = edate - datetime.timedelta(days=5*365)
            df_stock = web.DataReader(stock,'yahoo',sdate,edate)
            return(df_stock)
        except:
            time.sleep(randint(1,12))
            print('Error reading Yahoo KS - number of tries=',ntries)
        finally:
            ntries += 1 

    return(df_stock)    

df = safe_read_yahoo_finance('GOOG')
print(df)

#Creating a moving average of 30 days from the data scrapped
short_rolling = df.rolling(window=30).mean()
#Re-naming the column names
short_rolling.columns = ['Open (MA_30)', 'High(MA_30)', 'Low(MA_30)', 'Close(MA_30)','Adj Close(MA_30)','Volume(MA_30)']
#Concatenating original scrapped values with MA(30) values
result = pd.concat([df, short_rolling], axis=1).dropna()
result.to_excel('Goog-scrapped_MovingAverage.xlsx')
result.head()





