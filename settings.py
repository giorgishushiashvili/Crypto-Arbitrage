'''
    here will be included Control Variables
'''
#Crypto pairs that needs to be reworked
cryptos = [
    "BTCUSDT",
    "ETHUSDT"
]
futures = {
    "BTCUSDT":"BTCUSDT_210625",
    "ETHUSDT":"ETHUSDT_210625"
}

#Logic Settings
CORREL = 95 # if correlation between futures and spot is smaller enter the trade
TAKEPROFIT = 0.5 #% of initial ivestment converted to profit
