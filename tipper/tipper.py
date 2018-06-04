import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_username = 'bwsrpc'
rpc_password = 'qwert1'
rpc_ip = '127.0.0.1'
rpc_port = 43123
api_address= "https://www.worldcoinindex.com/apiservice/ticker?key=611jB7RdfZnnCqGMxO5p9D5drF5ZhI&label=bwsbtc&fiat=btc"

con = AuthServiceProxy('http://%s:%s@%s:%i'%(rpc_username, rpc_password, rpc_ip, rpc_port))
api = requests.get(api_address)

#Tip commands
def validateAddress(address):
    validate = con.validateaddress(address)
    return validate['isvalid'] #Returns True or False

def getAddress(account):
    return con.getaccountaddress(account)

def getBalance(account,minconf=1):
    return con.getbalance(account,minconf)

def withdraw(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        return con.sendfrom(account,destination,amount)

def tip(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        con.move(account,destination,amount)

def rain(account,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        accounts = con.listaccounts()
        eachTip = amount / len(accounts)
        for ac in accounts:
            tip(account,ac,eachTip)
        return eachTip

#API commands
def getPrice(amount=1,full=0,satoshi=0,refresh=0):
    global api
    r = api.json()['Markets'][0]
    price_btc = float(r['Price'])
    price_btcusd = float(requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]['price_usd'])
    price = float(price_btc * price_btcusd)

    if refresh:
        print('Fetching price from API')
        api = requests.get(api_address)
        r = api.json()['Markets'][0]
        price_btc = float(r['Price'])
        price_btcusd = float(requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]['price_usd'])
        price = float(price_btc * price_btcusd)
    if satoshi:
        return float("%.8f"%(price_btc*amount))
    elif full:
        return float("%.8f"%(price*amount))
    else:
        return float("%.4f"%(price*amount))
