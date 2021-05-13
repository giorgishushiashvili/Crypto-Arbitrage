import pandas as pd

#This class will be used to display information regarding balance and open positions
class interface:
    def __init__(self,app):
        self.app = app
    def SpotBalance(self,ticker):
        return self.app.GetAccountBalance(ticker=ticker)
    def FutureBalance(self,ticker):
        return self.app.Futures_Balance(ticker=ticker)
    def FuturePositions(self,ticker):
        data = self.app.Futures_currentPosition(ticker)
        return data
        
        
    def display(self):
        print(
                "-------------Spot Balance-------------\n",
                "\n",
                "USDT:",
                round(self.SpotBalance("USDT"),5),
                "BTC: ",
                round(self.SpotBalance("BTC"),5),
                "ETH: ",
                round(self.SpotBalance("ETH"),5),
                "\n",
                "\n-------------Futures balance------------- \n",
                "\n",
                "USDT:",
                round(self.FutureBalance("USDT"),5),
                "\n",
                "\n-------------TRADES------------- \n",
                self.FuturePositions("BTCUSDT_210625"),
                "\n",
                self.FuturePositions("ETHUSDT_210625"),
        )