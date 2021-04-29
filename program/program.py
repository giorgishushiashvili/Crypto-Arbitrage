#My libraries
import program.calculations as calcs
#python libraries
import statistics
import pandas as pd
import time

def GetTradingAmount(app):
    try:
        USDT = app.GetAccountBalance()
        return round(USDT/2-0.00005,4)
    except Exception as e:
        app.additlog("Error",["GetTradingAmount",e])
        return 0 

def OpenPosition(app, ticker, FuturesTicker, amount):
    try:
        tickerP = float(app.MarketDepth(ticker)[0][0][0])
        FuturesP = float(app.futures_MarketDepth(FuturesTicker)[1][0][0])
        app.Order(
            ticker,
            round(amount/tickerP-0.0005,3)
        )
        app.futures_order(
            FuturesTicker,
            "SELL",
            "MARKET",
            round(amount/FuturesP-0.0005,3)
        )
        app.additlog('trades',[ticker,tickerP,FuturesP,round(amount/tickerP-0.0005,3),round(amount/FuturesP-0.0005,3)])
    except Exception as e:
        print(e)
        app.additlog("Error",["OpenPosition",e])

#TODO this method is not finished
def ClosePosition(app,ticker,FuturesTicker): 
    try:
        amount = 0
        #TODO make better flow control
        if ticker == "ETHUSDT":
            amount = app.GetAccountBalance(ticker="ETH")
        elif ticker == "BTCUSDT":
            amount = app.GetAccountBalance(ticker="BTC")
        app.Order(
            ticker=ticker,
            quantity=amount,
            BUY=False
        )
        app.futures_order(
            ticker=FuturesTicker,
            side="BUY",
            types="MARKET",
            quantity=pd.read_csv("logs/trades.csv").tail(1)['amount2'].values[0]
        )
    except Exception as e:
        app.additlog("Error",["OpenPosition",e])




#This will single flow of the program.
def StartTrading(app,ticker,FuturesTicker):
    Enter_Trade = calcs.STDEV(app,ticker,FuturesTicker)
    shouldTrade = calcs.ShouldTrade(app,ticker,FuturesTicker)
    if Enter_Trade and shouldTrade:
        amount = GetTradingAmount(app) # half amount of my account
        app.TransferFunds(amount=amount,types=1) # Transfer half amount in the futures account
        OpenPosition(app, ticker, FuturesTicker, amount) # Open Position
        app.additlog('position',["O"])
        app.EmailMe("Trading","Started Trading on pair"+str(ticker))
    else:
        print("Waiting")

def EndTrading(app,ticker,FuturesTicker):
    #variables
    exitTrade = calcs.ExitTrade(app,ticker,FuturesTicker)
    if exitTrade:
        ClosePosition(app,ticker,FuturesTicker)
        balance = app.Futures_Balance()
        app.TransferFunds(amount=balance,types=2)
        app.additlog('position',["C"])
        app.EmailMe("EndTrading","Ended Trading on pair"+str(ticker))
    else:
        print("Waiting")



def program(app,ticker,FuturesTicker):
    position = pd.read_csv("logs/position.csv").tail(1)['Position'].values[0]
    if position == "C":
        StartTrading(app,ticker,FuturesTicker)
    else:
        if ticker == pd.read_csv("logs/trades.csv").tail(1)['Ticker'].values[0]:
            print("Trading")
            EndTrading(app,ticker,FuturesTicker)

