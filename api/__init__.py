from requests import Session
from selenium import webdriver
import datetime
import threading
import json
from time import sleep

class API:
    def __init__(self, username, password):
        self.session = Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:0.9.4.1) Gecko/20020518 Netscape6/6.2.3"
        })
        self._username = username
        self._password = password
        # set to False to stop threads
        self._allow_threads = True
        self.rates = None
        self.reconnect()

        self._rates_thread = threading.Thread(target=self._rates_worker)
        self._rates_thread.start()
        #print(self.get_rates())
        #print(self.get_team())
        #transaction = self.transaction("usd", 69, "ETH")
        #print(transaction)
        #breakpoint()
        #print(self.confirm_transaction(transaction["entity"]["transactionID"]))
        

    def reconnect(self):
        try:
            with open(".cookie", "r") as f:
                cookie = json.load(f)
                for k, v in cookie.items():
                    self.session.cookies[k] = v
                if self.session.get("https://platform.cryptobrawl.pl/api/rates", verify=False).status_code == 200:
                    print("Got cached!")
                    return
        except:
            print("Reconnecting!")
            driverOpts = webdriver.FirefoxOptions()
            driverOpts.headless = True
            driver = webdriver.Firefox(options=driverOpts)
            driver.get("https://platform.cryptobrawl.pl/ui/home")
            sleep(2)
            driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[2]/div/button").click()
            sleep(2)
            print("Logging in!")
            driver.find_element_by_id("email").send_keys(self._username)
            driver.find_element_by_id("password").send_keys(self._password)
            driver.find_element_by_id("cd_login_button").click()
            sleep(2)
            cookie_json = {}
            for cookie in driver.get_cookies():
                cookie_json[cookie['name']] = cookie['value']
                self.session.cookies[cookie['name']] = cookie['value']
            driver.close()
            with open(".cookie", "w+") as f:
                json.dump(cookie_json, f)
            print("I'm in!")

    def get_rates(self):
        return self.session.get("https://platform.cryptobrawl.pl/api/rates", verify=False).json()

    def get_team(self):
        return self.session.get("https://platform.cryptobrawl.pl/api/team", verify=False).json()

    def transaction(self, soldCurrency: str, soldAmount, bought: str):
        request = self.session.post(
                "https://platform.cryptobrawl.pl/api/transactions",
                json={
                    "tradingData": {
                        "boughtCurrency": bought.upper(),
                        "soldAmount":     str(soldAmount), 
                        "soldCurrency":   soldCurrency.upper()
                    }
                },
                verify=False)
        print(request.text)
        return request.json()

    def confirm_transaction(self, transaction_id: str):
        return self.session.post(
                "https://platform.cryptobrawl.pl/api/transactions/{}".format(transaction_id),
                verify=False
            ).json()

    def _rates_worker(self):
        while self._allow_threads:
            try:
                print("Getting rates!")
                rates = self.get_rates()
                self.rates = rates["entity"]
                update_again_at = datetime.datetime.fromtimestamp(rates["metadata"]["expiresAt"])
                time_left = update_again_at - datetime.datetime.now()
                print("Waiting", time_left.total_seconds())
                sleep(time_left.total_seconds() + 2)
            except Exception as e:
                print("_rates_worker:", e, flush=True)
                sleep(10)

    def __del__(self):
        print("Killing threads")
        self._allow_threads = False
        self._rates_thread.join()









