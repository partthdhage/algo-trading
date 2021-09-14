import logging

from kiteconnect import KiteConnect
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

from datetime import datetime, timedelta

if __name__ == '__main__':

    api_key = open('api_key.txt', 'r').read()
    api_secret = open('api_secret.txt', 'r').read()

    kite = KiteConnect(api_key=api_key)
    ##access_token = open('access_token.txt','r').read()

    print(kite.login_url())
    data = kite.generate_session("request_token_here", api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    ##print(data['access_token'])

    with open('access_token.txt','w') as ak:
        ak.write(data['access_token'])

    from_date = datetime.strftime(datetime.now()-timedelta(100),'%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    interval = '5minute'

    tokens = {738561:'RELIANCE', 341249:'HDFCBANK'}

    while True:
        if(datetime.now().second==0) and (datetime.now().minute %5 ==0):
            for token in tokens:
                records = kite.historical_data(token, from_date=from_date, to_date=to_date, interval=interval)
                df = pd.DataFrame(records)
                df.drop(df.tail(1).index, inplace=True)

                open = df['open'].values
                high = df['high'].values
                low = df['low'].values
                close = df['close'].values
                volume = df['volume'].values

                sma5 = talib.SMA(close,5)
                sma20 = talib.SMA(close,20)

                print(sma5[-1])
                print(sma20[-1])

                price = kite.ltp('NSE:' + tokens[token])
                print(price)

                ltp = price['NSE:' + tokens[token]]['last_price']

                if(sma5[-2]<sma20[-20]) and (sma5[-1]>sma20[-1]):

                    buy_order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
                    exchange=kite.EXCHANGE_NSE, order_type=kite.ORDER_TYPE_MARKET, tradingsymbol=tokens[token], transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=1, validity=kite.VALIDITY_DAY, product = kite.PRODUCT_MIS)
                    print(kite.orders())

                if(sma5[-2]>sma20[-20]) and (sma5[-1]<sma20[-1]):

                    sell_order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
                    exchange=kite.EXCHANGE_NSE, order_type=kite.ORDER_TYPE_MARKET, tradingsymbol=tokens[token], transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=1, validity=kite.VALIDITY_DAY, product = kite.PRODUCT_MIS)
                    print(kite.orders())
                    






    