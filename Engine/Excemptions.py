from binance.client import Client
import API
import time
import win32api

# This method will be the one who is identifing the error from binance and most importantly use correct predefined method to respond.
def handlingProcess(e):
    if str(e) == "APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.":
        client = Client(API.API, API.SECRET)
        changeTime(client)
        print("Work in progress")
    elif str(e) == "APIError(code=-1021): Timestamp for this request is outside of the recvWindow.":
        client = Client(API.API, API.SECRET)
        changeTime(client)
        print("Work in progress")
    elif str(e) == "APIError(code=-2010): Account has insufficient balance for requested action.":
        client = Client(API.API, API.SECRET)
        ETHBALANCE = client.get_asset_balance(asset='ETH')
        available_balance_ETH = float(ETHBALANCE['free'])
        print(available_balance_ETH)
    elif str(e) == "index out of bounds":
        print("Waiting - Currently no Resistance or Support level")
    else:    
        print(e)
        print("Error is not part of exemptions")


# Here will go code that will handle different errors which will be encountered during the testing phase
# each error will have different method
def changeTime(client):
    local_time1 = int(time.time() * 1000)
    server_time = client.get_server_time()
    diff1 = server_time['serverTime'] - local_time1
    local_time2 = int(time.time() * 1000)
    diff2 = local_time2 - server_time['serverTime']
    print("local1: %s server:%s local2: %s diff1:%s diff2:%s" % (local_time1, server_time['serverTime'], local_time2, diff1, diff2))

    
    #Correct Local time and adjust it to server time
    servTime=int(server_time['serverTime']) - 14400000
    servTime2=servTime/1000
    LocalTime=time.localtime(int(servTime2))
    win32api.SetSystemTime(LocalTime[0],LocalTime[1],0,LocalTime[2],LocalTime[3],LocalTime[4],LocalTime[5],0)