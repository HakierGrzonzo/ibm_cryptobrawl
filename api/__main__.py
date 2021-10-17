from api import API
import time
import datetime
import random
from .notifications import send_finished, send_going_to_start

TARGET_PROFIT = .1 # .1 - 10% profitu przy odpaleniu
WARNING_TIME = 600 # ile sekund przed handlem mam wysłać przypomnienie

while True:
    api = API("grzekop680@student.polsl.pl", "tu_wpisz_swoje_hasło_xd")
    bought_eth = 0
    bought_btc = 0
    team = api.get_team()
    usd = round(float(team['entity']['balance']['currencies']['usd']) * .8)
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
        try:
            # metoda Kamila
            print(iteration)
            iteration += 1
            roundedDiffrenceETH = round(rates['entity'][3]["rate"], 6) * rates['entity'][1]["rate"]
            roundedDiffrenceBTC = round(rates['entity'][2]["rate"], 6) * rates['entity'][0]["rate"]
            if roundedDiffrenceETH > 1.0008:
                print("start ETH trade because rate is:", roundedDiffrenceETH, flush=True)
                transaction = api.transaction('usd', usd, 'eth')
                if api.confirm_transaction(transaction).status_code == 200:
                    # ibm zwraca hajs jako string w json'ie, WTF!
                    bought_eth += float(transaction['entity']['boughtAmount'])
                    usd = 0
            elif roundedDiffrenceBTC > 1.0008:
                print("start BTC trade because rate is:", roundedDiffrenceBTC)
                transaction = api.transaction('usd', usd, 'btc')
                if api.confirm_transaction(transaction).status_code == 200:
                    # ibm zwraca hajs jako string w json'ie, WTF!
                    bought_btc += float(transaction['entity']['boughtAmount'])
                    usd = 0
            # sleep do sprzedaży!
            try:
                time.sleep(7 + random.randint(0, 10))
            finally:
                # Even if you press ctrl-c, try selling crypto
                if bought_eth > 0:
                    transaction = api.transaction('eth', bought_eth, 'usd')
                    if api.confirm_transaction(transaction).status_code == 200:
                        usd += round(float(transaction['entity']['boughtAmount']))
                        print(f"Sprzedałem {bought_eth}ETH za {usd}USD\t PROFIT: {usd - started_usd}USD", flush=True)
                        bought_eth = 0
                elif bought_btc > 0:
                    transaction = api.transaction('btc', bought_btc, 'usd')
                    if api.confirm_transaction(transaction).status_code == 200:
                        usd += round(float(transaction['entity']['boughtAmount']))
                        print(f"Sprzedałem {bought_btc}BTC za {usd}USD\t PROFIT: {usd - started_usd}USD", flush=True)
                        bought_btc = 0
            # Jak zarobisz wystarczająco dużo do wypierdalaj
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




