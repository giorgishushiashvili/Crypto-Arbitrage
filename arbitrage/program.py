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
    position = pd.read_csv("logs/position.csv").tail(1)['Position'].values[0]
    if position == "B":
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
            print("WOW")
        print(Maxdev," ",dt.tail(1)['diff'].values[0])
    #app.futures_order("ETHUSDT_210625","SELL","MARKET",0.01)
    #app.futures_order("ETHUSDT_210625","BUY","MARKET",0.01)