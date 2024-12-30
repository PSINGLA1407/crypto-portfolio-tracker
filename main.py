import requests

def get_eth_balance(wallet_address, api_key):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

wallet = "0xbE8860C3082C579D61A7D42c8E600e4f52b339a3"
api_key = ""
print(get_eth_balance(wallet, api_key))
