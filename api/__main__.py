from api import API
import time

api = API("grzekop680@student.polsl.pl", "tu_wpisz_swoje_hasło_xd")

while True:
    print(api.rates, flush=True)
    time.sleep(20)

