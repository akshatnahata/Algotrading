from kiteext import KiteExt 
import json 
import pandas as pd 
import logging 
from time import sleep 
import sys 
user = json.loads(open('userzerodha.json', 'r').read().rstrip()) 
 
# NOTE contents of above 'userzerodha.json' must be as below 
# { 
#     "user_id": "AB1234", 
#     "password": "P@ssW0RD", 
#     "twofa": "TWOFA123456" 
# } 
 
# NOTE Following way is also ok 
# kite.login_with_credentials(user_id, password, twofa) 
 
kite = KiteExt() 
kite.login_with_credentials( 
    userid=user['user_id'], password=user['password'], twofa=user['twofa']) 
#print(kite.profile()) 
#print(kite.positions()) 
#print(kite.orders()) 
#print(kite.ltp("NSE:SBIN")) 
#print(kite.ohlc("NSE:SBIN")) 
 
 
########################################################################### 
# 1- Block to get Banknifty Quote 
# 2- Block to calculate ATM Strike Price 
########################################################################### 
bnf_dictionary = kite.quote(["NSE:NIFTY BANK"]) 
last_tradeprice = bnf_dictionary.get('NSE:NIFTY BANK', {}).get('last_price') 
ATM_strike = int(round(last_tradeprice,-2)) 
 
 
############################################################# 
## Returns the list of FNO stocks as well as Call and Put strike price for Straddle 
################################################ 
 
def get_FNO_Stocks(): 
    fno_instruments = kite.instruments(exchange = "NFO") 
    fno_names_df = pd.DataFrame(fno_instruments,index=None) 
    fno_names_df = fno_names_df[fno_names_df.name=='BANKNIFTY'] 
    fno_names_df = fno_names_df[fno_names_df.strike == ATM_strike] 
    fno_names_df = fno_names_df.sort_values(by='expiry').head(2) 
    call_strike_symbol =fno_names_df[fno_names_df.instrument_type=='CE'].tradingsymbol.values[0] 
    put_strike_symbol = fno_names_df[fno_names_df.instrument_type == 'PE'].tradingsymbol.values[0] 
    #fno_names =  fno_names_df["tradingsymbol"].unique() 
    return (call_strike_symbol,put_strike_symbol) 
 
 
callPut_symbol = get_FNO_Stocks() 
#print(callPut_symbol) 
 
def placeorderstradlle(callPut_symbol): 
    #print(callPut_symbol[0]) 
    #print(callPut_symbol[1]) 
    lot_size = 25 
 
    try: 
        callshortorder_id = kite.place_order(tradingsymbol=callPut_symbol[0], quantity=lot_size, transaction_type=kite.TRANSACTION_TYPE_SELL, 
                                    exchange=kite.EXCHANGE_NFO, order_type=kite.ORDER_TYPE_MARKET, 
                                    product=kite.PRODUCT_MIS, variety=kite.VARIETY_REGULAR) 
        putshortorder_id = kite.place_order(tradingsymbol=callPut_symbol[1], quantity=lot_size, transaction_type=kite.TRANSACTION_TYPE_SELL, 
                                    exchange=kite.EXCHANGE_NFO, order_type=kite.ORDER_TYPE_MARKET, 
                                    product=kite.PRODUCT_MIS, variety=kite.VARIETY_REGULAR) 
 
        logging.info("call short Order placed. ID is: {}".format(callshortorder_id)) 
        logging.info("Put Short Order placed. ID is: {}".format(putshortorder_id)) 
        return "Success" 
        # logging.info("Order placement failed: {}".format(e)) 
    except Exception as e: 
        print("Unexpected error:", sys.exc_info()[0]) 
        logging.info("Order placement failed: {}".format(e))