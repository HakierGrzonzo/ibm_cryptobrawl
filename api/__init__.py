from requests import Session
from selenium import webdriver
from time import sleep

class API:
    def __init__(self, username, password):
        self.session = Session()
        self._username = username
        self._password = password
        self.reconnect()
        print(self.get_rates())
        print(self.get_team())
        transaction = self.transaction("usd", 69, "ETH")
        print(transaction)
        #breakpoint()
        print(self.confirm_transaction(transaction["entity"]["transactionID"]))
        

    def reconnect(self):
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
        for cookie in driver.get_cookies():
            self.session.cookies[cookie['name']] = cookie['value']
        driver.close()
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





