import json
import requests

def main():
    # importData()
    formatting()

def importData():
    InfoFile = open("exchangeInfo.json","w")
    
    url = "https://api.binance.com/api/v3/exchangeInfo"
    payload={}
    headers = {}

    print("Getting exchange information from Binance API...")
    response = requests.request("GET", url, headers=headers, data=payload)

    print("Writing information to exchangeInfo.json...")
    InfoFile.write(response.text)
    InfoFile.close()

def formatting():
    DataFile = open("exchangeInfo.json","r")
    print("Formatting data to fit gekko binance-markets.json")
    RawData = DataFile.read()
    Data = json.loads(RawData)
    Symbols = Data['symbols']
    sym_len = len(Symbols) - 1

    while sym_len>0:
        print(Symbols[sym_len]['symbol'])
        sym_len = sym_len - 1

if __name__ == "__main__":
    main()