LimitOrderIds=[]
symbolCode=""
avg_price=0
SL = 0          
def order_place(kite,symbol):
    symbolCode = symbol
    print(symbolCode)
    try:
        EntryOrderId = kite.place_order(tradingsymbol=symbol,exchange=kite.EXCHANGE_NFO,transaction_type=kite.TRANSACTION_TYPE_SELL,
                            quantity=50,variety=kite.VARIETY_REGULAR,order_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_MIS)
        sleep(5)
        avg_price = 0
        res = kite.orders()
        for row in res:
            if row['order_id'] == EntryOrderId:
                avg_price = row['average_price']
                break
        Utils.telegram_bot_sendtext("Entry Price = "+str(avg_price))

        stopLossOrder = kite.place_order(tradingsymbol=symbol,exchange=kite.EXCHANGE_NFO,
            transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=50,variety=kite.VARIETY_REGULAR,
            order_type=kite.ORDER_TYPE_SL,product=kite.PRODUCT_MIS, price=Utils.roundToNSEPrice(1.2 * int(avg_price) +1),  
            trigger_price=Utils.roundToNSEPrice(1.2 * int(avg_price)))
        LimitOrderIds.append(stopLossOrder)
def ModifySlOrder(kite,orderid,symbol):
    ltp= kite.ltp(['NFO:'+symbol]) ['NFO:'+symbol]['last_price']
    print(ltp)
    if ltp < (avg_price-1) :
        avg_price=avg_price-1
        SL=SL-1
        ModifySlOrderId = kite.modify_order(quantity=50,order_id=orderid,variety=kite.VARIETY_REGULAR,order_type=kite.ORDER_TYPE_SL, 
                                            price=SL+1, trigger_price=SL)
def CompleteLimitOrder(kite):
    ModifySlOrder(kite,LimitOrderIds[0],symbolCode)
               
