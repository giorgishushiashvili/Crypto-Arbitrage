import Engine.engine as engine
import Engine.Interface as Interface
import Engine.Excemptions as Exemptions
import program.program as program
import pandas as pd
import settings
import time


#This is entry point for the program
def main():
    #Create apps
    app = engine.Market()
    while 1:
        try:
            t1 = time.time_ns()
            Interface.interface(app).display()
            for cr in settings.cryptos:
                program.program(app,cr,settings.futures[cr])
            t2 = time.time_ns()
            print((t2 - t1)/1000000)
            time.sleep(2)
        except Exception as e:
            Exemptions.handlingProcess(e)
            time.sleep(1)
        

if __name__=="__main__":
    main()