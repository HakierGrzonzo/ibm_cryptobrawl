from api import API
import time
import datetime
import random
from api.coingecko import get_price_data

TARGET_PROFIT = .1 # .1 - 10% profitu przy odpaleniu
WARNING_TIME = 600 # ile sekund przed handlem mam wysłać przypomnienie

logfile = open("logfile.tsv", "w+")

iteration = 0
while True:
    api = API("grzekop680@student.polsl.pl", "ju4wk7gTRFxFdtb")
    bought_ratio_eth = 0
    bought_ratio_btc = 0
    team = api.get_team()
    usd = round(float(team['entity']['balance']['currencies']['usd']) * .99)
    bought_btc = float(team['entity']['balance']['currencies']['btc'])
    if bought_btc > 0:
        transaction = api.transaction('btc', bought_btc, 'usd')
        if api.confirm_transaction(transaction).status_code == 200:
            print("Sold BTC")
            bought_btc = 0
            usd += float(transaction['entity']['boughtAmount'])
    bought_eth = float(team['entity']['balance']['currencies']['eth'])
    if bought_eth > 0:
        transaction = api.transaction('eth', bought_eth, 'usd')
        if api.confirm_transaction(transaction).status_code == 200:
            print("Sold ETH")
            bought_eth = 0
            usd += float(transaction['entity']['boughtAmount'])
    #usd = 10000
    started_usd = usd
    print("Beggining trade with", usd, "USD!", flush=True)
    print("\tTarget is", usd * (TARGET_PROFIT + 1), "USD", flush=True)
    rates = api.get_rates()
    time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
    if time_to_next_update.total_seconds() < 10:
        # skip first period if we are late
        time.sleep(max(2, time_to_next_update.total_seconds()))
        rates = api.get_rates()
    print("Synchronizacja z patolą osiągnięta, zaczynam ojebywać IBM", flush=True)
    while True:
        print(iteration, flush=True)
        iteration += 1
        try:
            bitcoin, ethereum = get_price_data()
            bitcoin_ibm = rates['entity'][0]["rate"]
            ethereum_ibm = rates['entity'][1]['rate']
            if (
                    bought_btc > 0 and (
                        (
                            abs(bitcoin_ibm - bought_ratio_btc) > 1 and
                            abs(bitcoin_ibm - bitcoin['usd']) < 1
                        ) or
                        bitcoin['usd'] < bought_ratio_btc
                    )
                ):
                transaction = api.transaction('btc', bought_btc, 'usd')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Sold BTC")
                    bought_btc = 0
                    usd += float(transaction['entity']['boughtAmount'])
                    print("PROFIT:", usd - started_usd)
            if (
                    bought_eth > 0 and (
                        (
                            abs(ethereum_ibm - bought_ratio_eth) > .5 and
                            abs(ethereum_ibm - ethereum['usd']) < 1
                        ) or
                        ethereum['usd'] < bought_ratio_eth
                    )
                ):
                transaction = api.transaction('ETH', bought_eth, 'usd')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Sold ETH")
                    bought_eth = 0
                    usd += float(transaction['entity']['boughtAmount'])
                    print("PROFIT:", usd - started_usd)
            print(
                    iteration,
                    bitcoin['usd'],
                    ethereum['usd'],
                    bitcoin_ibm,
                    ethereum_ibm,
                    usd,
                    bought_btc,
                    bought_eth,
                    sep="\t",
                    file=logfile,
                    flush=True
                )
            time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
            time.sleep(max(1, time_to_next_update.total_seconds() * .75))
            # second half
            bitcoin, ethereum = get_price_data()
            if (
                    bitcoin['usd'] - bitcoin_ibm > 7 and 
                    usd > 0 and
                    (ethereum['usd'] - ethereum_ibm) / ethereum['usd'] < (bitcoin['usd'] - bitcoin_ibm) / bitcoin['usd']
                    ):
                # press advantage
                transaction = api.transaction('usd', usd, 'btc')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Bought BTC")
                    bought_btc += float(transaction['entity']['boughtAmount'])
                    usd = 0
                    bought_ratio_btc = bitcoin_ibm
            if ethereum['usd'] - ethereum_ibm > .01 and usd > 0:
                # press advantage
                transaction = api.transaction('usd', usd, 'eth')
                if api.confirm_transaction(transaction).status_code == 200:
                    print("Bought ETH")
                    bought_eth += float(transaction['entity']['boughtAmount'])
                    usd = 0
                    bought_ratio_eth = ethereum_ibm
            if (usd - started_usd) > (TARGET_PROFIT * started_usd):
                break
            print(
                    iteration + .5,
                    bitcoin['usd'],
                    ethereum['usd'],
                    bitcoin_ibm,
                    ethereum_ibm,
                    usd,
                    bought_btc,
                    bought_eth,
                    sep="\t",
                    file=logfile,
                    flush=True
                )
            # sleep do następnej transakcji
            time_to_next_update = api.get_update_datetime(rates) - datetime.datetime.now()
            time.sleep(max(2, time_to_next_update.total_seconds()))
            rates = api.get_rates()
        except Exception as e:
            print("EXCEPTION:", e)
            break
    print("Kończe trejdowanie", flush=True)
    time_to_sleep = datetime.timedelta(seconds=random.randint(10, 30))
    time_to_wake_up = datetime.datetime.now() + time_to_sleep
    time.sleep(time_to_sleep.total_seconds())

