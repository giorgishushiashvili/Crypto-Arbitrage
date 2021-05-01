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
            Interface.interface(app).display()
            for cr in settings.cryptos:
                program.program(app,cr,settings.futures[cr])
            time.sleep(5)
        except Exception as e:
            Exemptions.handlingProcess(e)
            time.sleep(1)
        

if __name__=="__main__":
    main()