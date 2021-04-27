#My libraries
import program.calculations as calcs
#python libraries
import statistics
import pandas as pd
import time

def GetTradingAmount(app):
    USDT = app.GetAccountBalance()
    return round(USDT/2-0.00005,4)

def OpenPosition(app, ticker, FuturesTicker, amount):
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
    app.additlog('position',["O"])
    app.additlog('trades',[ticker,tickerP,FuturesP,round(amount/tickerP-0.0005,3),round(amount/FuturesP-0.0005,3)])

#TODO this method is not finished
def ClosePosition(app,ticker,FuturesTicker): 
    amount = 0
    ERROR = False
    #TODO make better flow control
    if ticker == "ETHUSDT":
        amount = app.GetAccountBalance(ticker="ETH")
    elif ticker == "BTCUSDT":
        amount = app.GetAccountBalance(ticker="BTC")
    else:
        ERROR = True
        print("Error")
    if not ERROR:
        app.Order(
            ticker=ticker,
            quantity=amount,
            BUY=False
        )
        app.futures_order(
            FuturesTicker,
            "BUY",
            "MARKET",
            pd.read_csv("logs/trades.csv").tail(1)['amount2'].values[0]
        )




#This will single flow of the program.
def StartTrading(app,ticker,FuturesTicker):
    app.additlog('position',["O"])
    Enter_Trade = calcs.STDEV(app,ticker,FuturesTicker)
    shouldTrade = calcs.ShouldTrade(app,ticker,FuturesTicker)
    if Enter_Trade and shouldTrade:
        amount = GetTradingAmount(app) # half amount of my account
        app.TransferFunds(amount=amount,types=1) # Transfer half amount in the futures account
        OpenPosition(app, ticker, FuturesTicker, amount) # Open Position
        print("Position Opened")
    else:
        print("Waiting")

def EndTrading(app,ticker,FuturesTicker):
    #variables
    exitTrade = calcs.ExitTrade(app,ticker,FuturesTicker)
    if exitTrade:
        ClosePosition(app,ticker,FuturesTicker)
        balance = app.Futures_Balance()
        app.TransferFunds(amount=balance,types=2)
    else:
        print("Waiting")



def program(app,ticker,FuturesTicker):
    position = pd.read_csv("logs/position.csv").tail(1)['Position'].values[0]
    if position == "C":
        StartTrading(app,ticker,FuturesTicker)
    else:
        EndTrading(app,ticker,FuturesTicker)

