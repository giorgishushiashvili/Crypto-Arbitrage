from binance.client import Client
import pandas as pd
import API

class Market:
    def __init__(self):
        self.client = Client(API.API, API.SECRET)
    #Connecting to server 
    '''
        This is function for the comman crypto market
    '''
    #get Order book for spot market
    def MarketDepth(self,ticker):
        depth = self.client.get_order_book(symbol=ticker)
        asks = pd.DataFrame(depth['asks'])
        bids = pd.DataFrame(depth['bids'])
        return [asks,bids]
    #get Market price for spot market
    def MarketPrice(self,ticker):
        data = self.client.get_recent_trades(symbol=ticker)
        return float(data[len(data)-1]['price'])
    #Getting history data for spot market
    def candles(self,ticker,Duration="1h",ago="2 day"):
        ducation = {
            "1m":Client.KLINE_INTERVAL_1MINUTE,
            "1h":Client.KLINE_INTERVAL_1HOUR,
            "1d":Client.KLINE_INTERVAL_1DAY,
        }
        dt = pd.DataFrame(self.client.get_historical_klines(ticker, ducation[Duration], ago+" ago UTC"))
        dt.columns = [
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore'
        ]
        return dt
    #Placing Market orders on spot market 
    def Order(self,ticker,quantity,BUY=True):
        if BUY:
            self.client.order_market_buy(
                symbol=ticker,
                quantity=quantity
            )
        else:
            self.client.order_market_sell(
                symbol=ticker,
                quantity=quantity
            )
    #get Account Balance for spot market
    def GetAccountBalance(self,ticker="USDT"):
        return float(self.client.get_asset_balance(asset=ticker)['free'])

    '''
        Comunication between furures and spot markets
    '''
    def TransferFunds(self,amount,types=1):
        #1 means from spot to futures
        #2 means from futures to spot
        self.client.futures_account_transfer(asset="USDT",amount=amount,type=types)

    '''
        This is functions for Futures crypto market
    '''
    #get history data for futures market
    def Futures_candles(self,ticker,interval='1h',limit=1500):
        dt = pd.DataFrame(self.client.futures_klines(symbol=ticker,interval=interval,limit=limit))
        dt.columns = [
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore'
        ]
        return dt
    
    #get order book for futures market 
    def futures_MarketDepth(self,ticker):
        depth = self.client.futures_order_book(symbol=ticker)
        asks = pd.DataFrame(depth['asks'])
        bids = pd.DataFrame(depth['bids'])
        return [asks,bids]
    #place orders on futures market
    def futures_order(self,ticker,side,types,quantity,price=0):
        if types=="LIMIT" and price != 0:
            self.client.futures_create_order(symbol=ticker,side=side,type=types,quantity=quantity,price=price,timeInForce="GTC")
        elif types=="MARKET":
            self.client.futures_create_order(symbol=ticker,side=side,type=types,quantity=quantity)
    
    #Gets balance of my futures asset
    def Futures_Balance(self,ticker="USDT"):
        dt = self.client.futures_account_balance()
        balance = 0
        for data in dt:
            if data['asset'] == ticker:
                balance = data['withdrawAvailable']
        return float(balance)
    
    def Futures_TradeList(self,ticker):
        return self.client.futures_account_trades(ticker=ticker)
    
    def Futures_currentPosition(self,ticker="BTCUSDT"):
        data = pd.DataFrame(self.client.futures_position_information())
        dt = 0
        for index, row in data.iterrows():
            if row['symbol'] == ticker:
                dt = row
        return dt
    '''
        This will be functions for error handling and Alert system
    '''
    #Add Log information
    def additlog (self,file_name, list_of_elem):
        from csv import writer
        # Open file in append mode
        with open("logs/"+file_name+".csv", 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)
    #send an email
    def EmailMe(self,title="No Title",Msg="This is empty email"):
        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        sender_email = API.SENDER_EMAIL
        receiver_email = API.RECEIVER_EMAIL
        password = API.PASSWORD_EMAIL

        message = MIMEMultipart("alternative")
        message["Subject"] = title
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """Hi Giorgi, \n\nYou have new message: \n{Message}""".format(Message=Msg)
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    #Get percent of real numbers
    def Pct(self,amount):
        return amount/100