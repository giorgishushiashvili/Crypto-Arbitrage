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
        AMOUNT = round(amount/FuturesP-0.0005,3)
        app.Order(
            ticker,
            AMOUNT
        )
        app.futures_order(
            FuturesTicker,
            "SELL",
            "MARKET",
            AMOUNT
        )
        app.additlog('trades',[ticker,tickerP,FuturesP,AMOUNT,AMOUNT])
    except Exception as e:
        print(e)
        app.additlog("Error",["OpenPosition",e])

#TODO this method is not finished
def ClosePosition(app,ticker,FuturesTicker): 
    try:
        amount = 0
        #TODO make better flow control
        if ticker == "ETHUSDT":
            amount = round(app.GetAccountBalance(ticker="ETH")-0.000005,5)
        elif ticker == "BTCUSDT":
            amount = round(app.GetAccountBalance(ticker="BTC")-0.0000005,6)
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
        app.EmailMe("Trading","Started Trading on pair "+str(ticker)+"\n"+" amount = "+str(amount))

def EndTrading(app,ticker,FuturesTicker):
    #variables
    exitTrade = calcs.ExitTrade(app,ticker,FuturesTicker)
    if exitTrade:
        ClosePosition(app,ticker,FuturesTicker)
        balance = app.Futures_Balance()
        app.TransferFunds(amount=balance,types=2)
        app.additlog('position',["C"])
        app.EmailMe("EndTrading","Ended Trading on pair "+str(ticker))



def program(app,ticker,FuturesTicker):
    position = pd.read_csv("logs/position.csv").tail(1)['Position'].values[0]
    if position == "C":
        StartTrading(app,ticker,FuturesTicker)
        time.sleep(1)
    else:
        if ticker == pd.read_csv("logs/trades.csv").tail(1)['Ticker'].values[0]:
            print("Trading")
            EndTrading(app,ticker,FuturesTicker)

