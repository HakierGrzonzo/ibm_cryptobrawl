from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_price_data():
    data = cg.get_price(
            ['bitcoin', 'ethereum'], 
            vs_currencies="usd", 
            include_last_updated_at='true'
        )
    return data['bitcoin'], data['ethereum']

if __name__ == "__main__":
    print(get_price_data())

