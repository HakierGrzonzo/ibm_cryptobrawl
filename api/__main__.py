from api import API
import time
import datetime
import random
from .notifications import send_finished, send_going_to_start
from .coingecko import get_price_data

TARGET_PROFIT = .1 # .1 - 10% profitu przy odpaleniu
WARNING_TIME = 600 # ile sekund przed handlem mam wysłać przypomnienie

while True:
    api = API("grzekop680@student.polsl.pl", "tu_wpisz_swoje_hasło_xd")
    bought_eth = 0
    bought_ratio_eth = 0
    bought_btc = 0
    bought_ratio_btc = 0
    team = api.get_team()
    usd = round(float(team['entity']['balance']['currencies']['usd']) * .95)
    #usd = 10000
    started_usd = usd
    print("Beggining trade with", usd, "USD!", flush=True)
    print("\tTarget is", usd * (TARGET_PROFIT + 1), "USD", flush=True)
    rates = api.get_rates()
    time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
    if time_to_next_update.total_seconds() < 30:
        # skip first period if we are late
        time.sleep(max(2, time_to_next_update.total_seconds()))
        rates = api.get_rates()
    print("Synchronizacja z patolą osiągnięta, zaczynam ojebywać IBM", flush=True)
    iteration = 0
    while True:
        print(iteration, flush=True)
        iteration += 1
        try:
            bitcoin_ibm = rates['entity'][0]["rate"]
            ethereum_ibm = rates['entity'][1]['rate']
            if bought_btc > 0 and bitcoin_ibm != bought_ratio_btc:
                transaction = api.transaction('btc', bought_btc, 'usd')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Sold BTC")
                    bought_btc = 0
                    usd += float(transaction['entity']['boughtAmount'])
                    print("PROFIT:", usd - started_usd)
            elif bought_eth > 0 and ethereum_ibm != bought_ratio_eth:
                transaction = api.transaction('ETH', bought_eth, 'usd')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Sold ETH")
                    bought_eth = 0
                    usd += float(transaction['entity']['boughtAmount'])
                    print("PROFIT:", usd - started_usd)
            time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
            time.sleep(max(1, time_to_next_update.total_seconds() - 15))
            bitcoin, ethereum = get_price_data()
            ibm_timestamp = rates['metadata']['expiresAt'] - 60
            if bitcoin['last_updated_at'] > ibm_timestamp and usd > 0:
                print("Got advantage in BTC")
                if bitcoin['usd'] > bitcoin_ibm:
                    # press advantage
                    transaction = api.transaction('usd', usd, 'btc')
                    if api.confirm_transaction(transaction).status_code == 200:
                        print("Bought BTC")
                        bought_btc += float(transaction['entity']['boughtAmount'])
                        usd = 0
                        bought_ratio_btc = bitcoin_ibm
            if ethereum['last_updated_at'] > ibm_timestamp:
                print("Got advantage in ETH")
                if ethereum['usd'] > ethereum_ibm and usd > 0:
                    # press advantage
                    transaction = api.transaction('usd', usd, 'eth')
                    if api.confirm_transaction(transaction).status_code == 200:
                        print("Bought ETH")
                        bought_eth += float(transaction['entity']['boughtAmount'])
                        usd = 0
                        bought_ratio_eth = ethereum_ibm
            if (usd - started_usd) > (TARGET_PROFIT * started_usd):
                break
            # sleep do następnej transakcji
            time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
            time.sleep(max(2, time_to_next_update.total_seconds() + random.randint(0, 4)))
            rates = api.get_rates()
        except Exception as e:
            print("EXCEPTION:", e)
            time.sleep(120)
            api.reconnect()
            rates = api.get_rates()
            time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
            if time_to_next_update.total_seconds() < 30:
                # skip first period if we are late
                time.sleep(max(2, time_to_next_update.total_seconds()))
                rates = api.get_rates()
            print("Got back in action!", flush=True)
    print("Kończe trejdowanie", flush=True)
    time_to_sleep = datetime.timedelta(hours=random.randint(2, 4), minutes=random.randint(0, 59))
    time_to_wake_up = datetime.datetime.now() + time_to_sleep
    print(f"Ide spać do {time_to_wake_up.isoformat()}", flush=True)
    send_finished(str(round(usd - started_usd)), time_to_wake_up.isoformat(sep=' '))
    time.sleep(time_to_sleep.total_seconds() - WARNING_TIME)
    send_going_to_start(time_to_wake_up.isoformat(sep=" "))
    time.sleep(WARNING_TIME)

