#This file will return True or False
#True - Take action
#False - Wait
import Engine.engine as engine
import settings as settings
import statistics
import pandas as pd
import numpy as np
'''
    Entering the trade
'''
def ShouldTrade(app,ticker,FuturesTicker):
    try:
        CurrentPrice = float(app.MarketDepth(ticker)[1][0][0])
        CurrentPrice_Futures = float(app.futures_MarketDepth(FuturesTicker)[0][0][0])
        print("CurrentPrice ",CurrentPrice," future Price ", CurrentPrice_Futures)
        if CurrentPrice * 1.01 < CurrentPrice_Futures:
            return True
        else:
            return False
    except Exception as e:
        app.additlog("Error",["ShouldTrade",e])
        return False

#this method does not give me max revenue
def Correl(app,ticker,futureTk):
    try:
        crypto = app.candles(ticker)['Close'].astype(float)
        futures = app.Futures_candles(futureTk,limit=48)['Close'].astype(float)
        dt = pd.DataFrame({
                "CRYPTO":crypto,
                "FUTURES":futures
        })
        CORREL = round(np.corrcoef(dt['FUTURES'],dt['CRYPTO'])[0][1]*100,2)
        if CORREL < settings.CORREL:
            return True
        else:
            return False
    except Exception as e:
        app.additlog("Error",["Correl",e])
        return False

#currently this method gives me max revenue
def STDEV(app,ticker,futureTk):
    try:
        crypto = app.candles(ticker)['Close'].astype(float)
        futures = app.Futures_candles(futureTk,limit=48)['Close'].astype(float)
        dt = pd.DataFrame({
                "CRYPTO":crypto,
                "FUTURES":futures
        })
        dt['diff'] = dt['FUTURES']-dt['CRYPTO']
        average = statistics.mean(dt['diff'])
        stdev = statistics.pstdev(dt['diff'])
        Maxdev = average + stdev
        print("Std - ",Maxdev)
        if Maxdev < dt.tail(1)['diff'].values[0]:
            return True
        else:
            return False
    except Exception as e:
        app.additlog("Error",["STDEV",e])
        return False

'''
    Exiting the trade
'''

def ExitTrade(app,ticker,FuturesTicker):
    try:
        #variables
        
        ActiveTrades = pd.read_csv('logs/trades.csv')
        price1 = ActiveTrades.tail(1)['Crypto'].values[0]
        price2 = ActiveTrades.tail(1)['Crypto_210625'].values[0]
        CurrentPrice = float(app.MarketDepth(ticker)[1][0][0])
        CurrentPrice_Futures = float(app.futures_MarketDepth(FuturesTicker)[0][0][0])
        AMOUNT1 = ActiveTrades.tail(1)['amount1'].values[0]
        AMOUNT2 = ActiveTrades.tail(1)['amount2'].values[0]

        #AMOUNT and Commisions
        profit1 = (AMOUNT1 * CurrentPrice - AMOUNT1 * price1) - (AMOUNT1 * CurrentPrice * app.Pct(0.1) + AMOUNT1 * price1 * app.Pct(0.1))
        profit2 = (AMOUNT2 * price2 - AMOUNT2 * CurrentPrice_Futures) - (AMOUNT2 * CurrentPrice_Futures * app.Pct(0.1) + AMOUNT2 * price2 * app.Pct(0.1))
        #P&L of both positions
        print(" profit 1 ",round(profit1,4)," profit 2 ",round(profit2,4)," Sum ",round(profit1 + profit2,4))
        if profit1 + profit2 + 200 > 200 * (1 + app.Pct(settings.TAKEPROFIT)):
            return True
        else:
            return False
    except Exception as e:
        app.additlog("Error",["ExitTrade",e])
        return False