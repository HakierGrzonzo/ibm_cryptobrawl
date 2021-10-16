from requests import Session
from selenium import webdriver
#from .coingecko import cg
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
        self.pre_rate_change_hooks = []
        self.after_rate_change_hooks = []
        self.realprice = None
        # set to False to stop threads
        self._allow_threads = True
        self.rates = None
        self.reconnect()
        self._rates_thread = threading.Thread(target=self._rates_worker)
        self._rates_thread.start()
       # self.pre_rate_change_hooks.append(self.test_worker)
        self.after_rate_change_hooks.append(self.earn_from_rounding)
        #Diffrent after_rate_change_hooksbetween actually value and calculated by IBM
        self.roundedDiffrenceETH = 0.0
        self.roundedDiffrenceBTC = 0.0

        #print(self.get_rates())
        #print(self.get_team())
        #transaction = self.transaction("usd", 69, "ETH")
        #print(transaction)
        #breakpoint()
        #print(self.confirm_transaction(transaction["entity"]["transactionID"]))

    def test_worker(self):
        print(self.realprice['bitcoin']['usd'], self.rates[0]['rate'])

    def earn_from_rounding(self):
        self.roundedDiffrenceETH = round(self.rates[3]["rate"], 6) * self.rates[1]["rate"]
        self.roundedDiffrenceBTC = round(self.rates[2]["rate"], 6) * self.rates[0]["rate"]
        how_much_to_buy = 213700
        print(self.rates)
        print(self.roundedDiffrenceETH)
        if(self.roundedDiffrenceETH>1.0008):
            print("start ETH treade because rate is: ", self.roundedDiffrenceETH)
            transaction = self.transaction("usd", how_much_to_buy, "ETH")
            self.confirm_transaction(transaction["entity"]["transactionID"])
            sleep(7)
            transaction = self.transaction("ETH", round(round(self.rates[3]["rate"], 6) * how_much_to_buy, 6), "usd")
            self.confirm_transaction(transaction["entity"]["transactionID"])
        if(self.roundedDiffrenceBTC>1.0008):
            print("start BTC treade because rate is: ", self.roundedDiffrenceBTC)
            transaction = self.transaction("usd", how_much_to_buy, "BTC")
            self.confirm_transaction(transaction["entity"]["transactionID"])
            sleep(7)
            transaction = self.transaction("BTC", round(round(self.rates[2]["rate"], 6) * how_much_to_buy, 6), "usd")
            self.confirm_transaction(transaction["entity"]["transactionID"])



    def reconnect(self):
        try:
            with open(".cookie", "r") as f:
                cookie = json.load(f)
                for k, v in cookie.items():
                    self.session.cookies[k] = v
                if self.session.get("https://platform.cryptobrawl.pl/api/rates", verify=False).status_code == 200:
                    print("Got cached!")
                    #return
        except:
            pass
        print("Reconnecting!")
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
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
            )

    def run_hooks(self, hooks):
        #self.realprice = cg.get_price(ids="bitcoin", vs_currencies="usd")
        for hook in hooks:
            hook()

    def _rates_worker(self):
        while self._allow_threads:
            try:
                print("Getting rates!")
                rates = self.get_rates()
                self.rates = rates["entity"]
                update_again_at = datetime.datetime.fromtimestamp(rates["metadata"]["expiresAt"])
                if not self._allow_threads:
                    break
                print("after rate hooks", flush=True)
                hook_thread = threading.Thread(target=self.run_hooks, args=(self.after_rate_change_hooks,))
                hook_thread.start()
                time_left = update_again_at - datetime.datetime.now()
                sleep(time_left.total_seconds() / 2 + 1)

                hook_thread.join()
                if not self._allow_threads:
                    break
                print("pre rate hooks", flush=True)
                hook_thread = threading.Thread(target=self.run_hooks, args=(self.pre_rate_change_hooks,))
                hook_thread.start()
                time_left = update_again_at - datetime.datetime.now()
                sleep(time_left.total_seconds() + 1)
                hook_thread.join()
            except Exception as e:
                print("_rates_worker:", e, flush=True)
                sleep(10)

    def __del__(self):
        print("Killing threads")
        self._allow_threads = False
        self._rates_thread.join()









