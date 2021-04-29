import Engine.engine as engine
import API
import time
import win32api

class ErrorHandilng:
    def __init__(self):
        self.client = engine.Market()
    def handlingProcess(self,e):
        if str(e) == "APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.":
            self.changeTime()
        elif str(e) == "APIError(code=-1021): Timestamp for this request is outside of the recvWindow.":
            self.changeTime()
        else:    
            self.client.additlog("NewError",e)

    def changeTime(self):
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