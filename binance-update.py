import json
import requests

def main():
    importData()
    formatData()

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

def formatData():
    DataFile = open("exchangeInfo.json","r")
    print("Formatting data to fit gekko binance-markets.json")
    RawData = DataFile.read()
    Data = json.loads(RawData)
    Symbols = Data['symbols']
    sym_len = len(Symbols) - 1
    count = 0
    _currencies = []
    _assets = []
    _markets = []

    while count < sym_len:
        _pair = []
        _minimalOrder = {
            "amount": 0,
            "price": 0,
            "order": 0
        }
        # print(Symbols[count]['filters'][2]['minQty'])
        if not Symbols[count]['baseAsset'] in _assets:
            _assets.append(Symbols[count]['baseAsset'])
        _pair.append(Symbols[count]['baseAsset'])
        if not Symbols[count]['quoteAsset'] in _currencies:
            _currencies.append(Symbols[count]['quoteAsset'])
        _pair.append(Symbols[count]['quoteAsset'])
        _minimalOrder['amount'] = float(Symbols[count]['filters'][2]['minQty'])
        _minimalOrder['price'] = float(Symbols[count]['filters'][0]['minPrice'])
        _minimalOrder['order'] = float(Symbols[count]['filters'][3]['minNotional'])
        _obj = {
            "pair": _pair,
            "minimalOrder": _minimalOrder
        }
        _markets.append(_obj)
        count += 1

    DataOutput = {
        "assets": _assets,
        "currencies": _currencies,
        "markets": _markets
    }

    OutputFile = open("binance-markets.json", "w")
    OutputFile.write(json.dumps(DataOutput, sort_keys=True, indent=4))
    OutputFile.close()
    print("Done.")

if __name__ == "__main__":
    main()