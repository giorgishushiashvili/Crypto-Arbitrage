import Engine.engine as engine
import program.program as program
import pandas as pd
import settings
import time

    
#This is entry point for the program
def main():
    app = engine.Market()
    for cr in settings.cryptos:
        program.program(app,cr,settings.futures[cr])

if __name__=="__main__":
    main()