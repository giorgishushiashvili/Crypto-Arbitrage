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
    def MarketDepth(self,ticker):
        depth = self.client.get_order_book(symbol=ticker)
        asks = pd.DataFrame(depth['asks'])
        bids = pd.DataFrame(depth['bids'])
        return [asks,bids]
    def MarketPrice(self,ticker):
        data = self.client.get_recent_trades(symbol=ticker)
        return float(data[len(data)-1]['price'])
    def candles(self,ticker,Duration="1h",ago="3 day"):
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

    '''
        This is functions for Futures crypto market
    '''
    def Futeres_candles(self,ticker,interval='1h',limit=1500):
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
    '''
        This will be functions for error handling
    '''
    #Add Log information
    def additlog (self,file_name, list_of_elem):
        from csv import writer
        # Open file in append mode
        with open("logs/"+file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)
    #send an email
    def SentAlert(self,title="No Title",Msg="This is empty email"):
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
