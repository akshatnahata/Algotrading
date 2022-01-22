# -*- coding: utf-8 -*-


from kiteconnect import KiteTicker, KiteConnect
import pandas as pd
import datetime as dt
import os

cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

def tokenLookup(instrument_df,symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    for symbol in symbol_list:
        token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
    return token_list

def tickerLookup(token):
    global instrument_df
    return instrument_df[instrument_df.instrument_token==token].tradingsymbol.values[0] 

def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1
        
def fetchOHLC(ticker,interval,duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data

def atr(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    return df['ATR'][-1]
        
def renkoOperation(ticks):
    for tick in ticks:
        try:
            ticker = tickerLookup(int(tick['instrument_token']))
            if renko_param[ticker]["upper_limit"] == None:
                renko_param[ticker]["upper_limit"] = float(tick['last_price']) + renko_param[ticker]["brick_size"]
                renko_param[ticker]["lower_limit"] = float(tick['last_price']) - renko_param[ticker]["brick_size"]
            if float(tick['last_price']) > renko_param[ticker]["upper_limit"]:
                gap = (float(tick['last_price'] - renko_param[ticker]["upper_limit"]))//renko_param[ticker]["brick_size"]
                renko_param[ticker]["lower_limit"] = renko_param[ticker]["upper_limit"] + (gap*renko_param[ticker]["brick_size"]) - renko_param[ticker]["brick_size"]
                renko_param[ticker]["upper_limit"] = renko_param[ticker]["upper_limit"] + ((1+gap)*renko_param[ticker]["brick_size"])
                renko_param[ticker]["brick"] = max(1,renko_param[ticker]["brick"]+(1+gap))
            if float(tick['last_price']) < renko_param[ticker]["lower_limit"]:
                gap = (renko_param[ticker]["lower_limit"] - float(tick['last_price']))//renko_param[ticker]["brick_size"]
                renko_param[ticker]["upper_limit"] = renko_param[ticker]["lower_limit"] - (gap*renko_param[ticker]["brick_size"]) + renko_param[ticker]["brick_size"]
                renko_param[ticker]["lower_limit"] = renko_param[ticker]["lower_limit"] - ((1+gap)*renko_param[ticker]["brick_size"])
                renko_param[ticker]["brick"] = min(-1,renko_param[ticker]["brick"]-(1+gap))
            print("{}: brick number = {},last price ={}, upper bound ={}, lower bound ={}"\
                  .format(ticker,renko_param[ticker]["brick"],tick['last_price'],renko_param[ticker]["upper_limit"],renko_param[ticker]["lower_limit"]))
        except Exception as e:
            print(e)
            pass 
    
    
#####################update ticker list######################################
tickers = ["ZEEL","WIPRO","VEDL","ULTRACEMCO","UPL","TITAN","TECHM","TATASTEEL",
           "TATAMOTORS","TCS","SUNPHARMA","SBIN","SHREECEM","RELIANCE","POWERGRID",
           "ONGC","NESTLEIND","NTPC","MARUTI","M&M","LT","KOTAKBANK","JSWSTEEL","INFY",
           "INDUSINDBK","IOC","ITC","ICICIBANK","HDFC","HINDUNILVR","HINDALCO",
           "HEROMOTOCO","HDFCBANK","HCLTECH","GRASIM","GAIL","EICHERMOT","DRREDDY",
           "COALINDIA","CIPLA","BRITANNIA","INFRATEL","BHARTIARTL","BPCL","BAJAJFINSV",
           "BAJFINANCE","BAJAJ-AUTO","AXISBANK","ASIANPAINT","ADANIPORTS"]
#############################################################################
renko_param = {}
for ticker in tickers:
    renko_param[ticker] = {"brick_size":round(atr(fetchOHLC(ticker,"5minute",15),200),2),"upper_limit":None, "lower_limit":None,"brick":0}
    
#create KiteTicker object
kws = KiteTicker(key_secret[0],kite.access_token)
tokens = tokenLookup(instrument_df,tickers)

def on_ticks(ws,ticks):
    renkoOperation(ticks)
    #print(ticks)

def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_LTP,tokens)
    
kws.on_ticks=on_ticks
kws.on_connect=on_connect
kws.connect()