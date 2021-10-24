from requests import Session
from selenium import webdriver
#from .coingecko import cg
import datetime
import threading
import json
from time import sleep
import urllib3

urllib3.disable_warnings()

class API:
    def __init__(self, username, password):
        self.session = Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:0.9.4.1) Gecko/20020518 Netscape6/6.2.3"
        })
        self._username = username
        self._password = password
        self.reconnect()

    def reconnect(self):
        """
        try:
            with open(".cookie", "r") as f:
                cookie = json.load(f)
                for k, v in cookie.items():
                    self.session.cookies[k] = v
                if self.session.get("https://platform.cryptobrawl.pl/api/rates", verify=False).status_code == 200:
                    print("Got cached!")
                    return
        except:
            pass
        """
        print("Reconnecting!")
        options = webdriver.FirefoxOptions()
        #options.headless = True
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
        print("I'm in!", flush=True)

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
        return request.json()

    def confirm_transaction(self, transaction_id):
        if not isinstance(transaction_id, str):
            try:
                transaction_id = transaction_id['entity']['transactionID']
            except KeyError as e:
                print(transaction_id)
                raise e
        return self.session.post(
                "https://platform.cryptobrawl.pl/api/transactions/{}".format(transaction_id),
                verify=False
            )

    def get_update_datetime(self, rates):
        return datetime.datetime.fromtimestamp(rates['metadata']['expiresAt'])

