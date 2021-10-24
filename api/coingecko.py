import requests

def get_price_data():
    bitcoin = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC")
    ethereum = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=ETH")
    correction = 1
    bitcoin_rate = {'usd': float(bitcoin.json()['data']['rates']['USD']) * correction}
    ethereum_rate = {'usd': float(ethereum.json()['data']['rates']['USD']) * correction}
    return bitcoin_rate, ethereum_rate

if __name__ == "__main__":
    print(get_price_data())

