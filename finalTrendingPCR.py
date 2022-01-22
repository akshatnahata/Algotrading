import requests
import pandas as pd
import time

url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

session = requests.Session()
cookies = session.cookies.get_dict()
request = session.get(url,headers=headers)
# print(cookies)
response = session.get(url,headers=headers,cookies=cookies).json()
rawdata=pd.DataFrame(response)
rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
# print(rawop)

def dataframe(rawop):
    data=[]
    for i in range(0,len(rawop)):
        calloi=calloichange= putoi=putoichange=0
        stp=rawop['strikePrice'][i]
        if(rawop['CE'][i]==0):
            calloi=calloichange=0
        else:
            calloi=rawop["CE"][i]["openInterest"]
            calloichange=rawop["CE"][i]["changeinOpenInterest"]
            cltp=rawop['CE'][i]['lastPrice']


        if(rawop['PE'][i]==0):
            putoi=putoichange=0
        else:
            putoi=rawop["PE"][i]["openInterest"]
            putoichange=rawop["PE"][i]["changeinOpenInterest"]
            pltp=rawop['PE'][i]['lastPrice']   

        opdata={
            'Call OI': calloi,'Call ltp':cltp,'Strike Price': stp,'Call OI Change':calloichange,
            'Put OI': putoi,'Put ltp':pltp,'Strike Price': stp,'Put OI Change':putoichange

        }     
        data.append(opdata)
    optionchain  = pd.DataFrame(data)
    return optionchain
def main():
    optionchain=dataframe(rawop)
# print(optionchain)

    TotalCallOI = optionchain['Call OI'].sum()
    TotalPutOI = optionchain['Put OI'].sum()
    print(f'PCR: {TotalPutOI/TotalCallOI}')

while True:
    main()
    time.sleep(180)




   
                



