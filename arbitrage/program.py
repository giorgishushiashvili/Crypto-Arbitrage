#My libraries
import Engine.engine as engine
#python libraries
import statistics
import pandas as pd
import time

app = engine.Market()

#TODO Here will be my arbitrage trading bot
#ETHUSDT_210625
def program():
    
    position =pd.read_csv("logs/position.csv").tail(1)['Position'].values[0]
    #if position == B than check if I should buy
    if position == "B":
        USDT = app.GetAccountBalance()
        ETHUSDT = app.candles("ETHUSDT")['Close'].astype(float)
        ETHUSDT_210625=app.Futures_candles("ETHUSDT_210625",limit=48)['Close'].astype(float)
        #analysis
        dt = pd.DataFrame({
            "ETHUSDT":ETHUSDT,
            "ETHUSDT_210625":ETHUSDT_210625
        })
        dt['diff'] = dt['ETHUSDT_210625']-dt['ETHUSDT']
        average = statistics.mean(dt['diff'])
        stdev = statistics.pstdev(dt['diff'])
        Maxdev = average + stdev
        if Maxdev < dt.tail(1)['diff'].values[0]:
            #TODO Add ability to buy asset and sell futures
            amount = round(USDT/2-0.00005,4)
            app.TransferFunds(amount=amount,types=1)
            #TODO This needs optimization
            app.Order(
                "ETHUSDT",
                round(amount/float(app.MarketDepth("ETHUSDT")[0][0][0])-0.005,2)
            )
            app.futures_order(
                'ETHUSDT_210625',
                "SELL",
                "MARKET",
                round(amount/float(app.futures_MarketDepth("ETHUSDT_210625")[1][0][0])-0.0005,3)
            )
            app.additlog("position.csv",'S')
            app.additlog("trades.csv",[
                "ETHUSDT",
                float(app.MarketDepth("ETHUSDT")[0][0][0]),
                float(app.futures_MarketDepth("ETHUSDT_210625")[1][0][0]),
                round(amount/float(app.MarketDepth("ETHUSDT")[0][0][0])-0.005,2),
                round(amount/float(app.futures_MarketDepth("ETHUSDT_210625")[1][0][0])-0.0005,3)
            ])

            app.EmailMe(title="Bought Asset",Msg="Asset Was Bought")
        print(Maxdev," ",dt.tail(1)['diff'].values[0])
    elif position == "S":
        ActiveTrades = pd.read_csv('logs/trades.csv')
        ticker = ActiveTrades.tail(1)['Ticker'].values[0]
        price1 = ActiveTrades.tail(1)['Crypto'].values[0]
        price2 = ActiveTrades.tail(1)['Crypto_210625'].values[0]
        CurrentPrice = float(app.MarketDepth(ticker)[1][0][0])
        CurrentPrice_Futures = float(app.futures_MarketDepth(ticker+"_210625")[0][0][0])

        profit1 = round(100 / price1 * (1 - 0.001) * CurrentPrice * (1 - 0.001)-0.005,2)
        profit2 = round(100 * price2 * (1 - 0.0004) / CurrentPrice_Futures * (1 - 0.0004)-0.005,2)
        print("profit1 ",profit1," profit2 ",profit2," SUM ",profit1 + profit2)
        if profit1 + profit2 > 201:
            if ticker == "ETHUSDT":
                amount = app.GetAccountBalance(ticker="ETH")
                app.Order(
                    ticker=ticker,
                    quantity=amount,
                    BUY=False
                )
                app.futures_order(
                    'ETHUSDT_210625',
                    "BUY",
                    "MARKET",
                    ActiveTrades.tail(1)['amount2'].values[0]
                    )

                app.additlog("position.csv",'B')
                app.additlog("trades.csv",[
                    "ETHUSDT",
                    CurrentPrice,
                    CurrentPrice_Futures,
                    amount,
                    ActiveTrades.tail(1)['amount2'].values[0]
                ])
                
            #TODO add transfer funds ability to the program
            balance = app.Futures_Balance()
            app.TransferFunds(amount=balance,types=2)
            app.EmailMe(title="Sold Asset",Msg="Asset Was Sold")
    
    