from urllib import response
import requests
import time
import pandas as pd
from datetime import datetime

def datetotimestamp(date):
    time_tuple = date.timetuple()
    timestamp = round(time.mktime(time_tuple))
    return timestamp

def timestamptodate(timestamp):
    return datetime.fromtimestamp(timestamp)


date = datetime.today()
start = datetotimestamp(datetime(2021,1,15))
end = datetotimestamp(datetime.today())
url = "https://priceapi.moneycontrol.com/techCharts/techChartController/history?symbol=23&resolution=5&from="+str(start)+"&to="+str(end)
# print(url)
resp = requests.get(url).json()
data = pd.DataFrame(resp)
date = []
for dt in data['t']:
    date.append({'Date':timestamptodate(dt)})

dt = pd.DataFrame(date)
# print(dt)
intraday_data = pd.concat([dt, data['o'],data['h'],data['l'],data['c'],data['v']],axis=1)
intraday_data.to_csv('banknifty.csv')