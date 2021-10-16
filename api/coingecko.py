from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
print(cg.get_price(ids='bitcoin', vs_currencies='usd'))

