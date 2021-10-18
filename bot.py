from datetime import date, datetime, timedelta
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from log import Log
from xpath import *
import pandas as pd
import undetected_chromedriver.v2 as uc

class SuchenMobileDe():

    def __init__(self):
        self.log = Log()
        self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0"
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = Chrome(executable_path='chromedriver93.0.4577.15_win32.exe', options=chrome_options)
        
    def __exWaitS(self):
        # Implicit waiting functions
        return WebDriverWait(self.driver, 5)
        
    def _click(self, element, msg=" "):
        # This functions is to just click stuff
        self.log.write_log("bot", msg)
        element.click()
        
    def _waiting(self, waitingTime, msg=" "):
        # Waiting for waitingTime seconds
        self.log.write_log("bot", msg)
        time.sleep(waitingTime)
    
    def login(self, vehicle_type="cars", price_from=-1, price_to=-1, registration_from=-1, registration_to=-1, kilometer_from=-1, kilometer_to=-1, provider="any"):
        if vehicle_type == "cars":
            self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0"
        elif vehicle_type == "motorcycles":
            self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?vc=Motorbike"
        self.driver.get(self.site_url)
        time.sleep(15)
        if price_from != -1:
            try:
                minPrice = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minPrice")),
                    message="timeout trying to find min price input",
                )
                minPrice.send_keys(price_from)
            except Exception as e:
                print(e)
                pass
        if price_to != -1:
            try:
                maxPrice = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxPrice")),
                    message="timeout trying to find max price input",
                )
                maxPrice.send_keys(price_to)
            except Exception as e:
                print(e)
                pass
        if registration_from != -1:
            try:
                minFirstRegistrationDate = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minFirstRegistrationDate")),
                    message="timeout trying to find min registration input",
                )
                minFirstRegistrationDate.send_keys(registration_from)
            except Exception as e:
                print(e)
                pass
        if registration_to != -1:
            try:
                maxFirstRegistrationDate = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxFirstRegistrationDate")),
                    message="timeout trying to find max registration input",
                )
                maxFirstRegistrationDate.send_keys(registration_to)
            except Exception as e:
                print(e)
                pass
        if kilometer_from != -1:
            try:
                minMileage = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minMileage")),
                    message="timeout trying to find min kilometer input",
                )
                minMileage.send_keys(kilometer_from)
            except Exception as e:
                print(e)
                pass
        if kilometer_to != -1:
            try:
                maxMileage = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxMileage")),
                    message="timeout trying to find max kilometer input",
                )
                maxMileage.send_keys(kilometer_to)
            except Exception as e:
                print(e)
                pass
        if provider == "any":
            try:
                anyRadio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation--ds")),
                    message="timeout trying to find any radio",
                )
                anyRadio.click()
            except Exception as e:
                print(e)
                pass
        if provider == "Private provider":
            try:
                private_provider_radio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_FSBO_ADS-ds")),
                    message="timeout trying to find private provider radio",
                )
                private_provider_radio.click()
            except Exception as e:
                print(e)
                pass
        if provider == "Dealers":
            try:
                dealerRadio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_DEALER_ADS-ds")),
                    message="timeout trying to find dealer radio",
                )
                dealerRadio.click()
            except Exception as e:
                print(e)
                pass
        if provider == "Company vehicles":
            try:
                company_vehicle_radio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_COMMERCIAL_FSBO_ADS-ds")),
                    message="timeout trying to find company vehicle radio",
                )
                company_vehicle_radio.click()
            except Exception as e:
                print(e)
                pass
        try:
            acceptBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "mde-consent-accept-btn")),
                message="timeout trying to find accept button",
            )
            acceptBtn.click()
        except Exception as e:
            print(e)
            pass
        try:
            searchBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "dsp-upper-search-btn")),
                message="timeout trying to find offer button",
            )
            # self.driver.execute_script("arguments[0].click();", offerBtn)
            searchBtn.click()
        except Exception as e:
            print(e)
            pass
            
    def start(self, minimal_photo_count=0):
        try:
            item = self.__exWaitS().until(
                ec.presence_of_element_located((By.CLASS_NAME, "cBox-body cBox-body--topResultitem dealerAd")),
                message="timeout trying to find top result item",
            )
            imageNum = item.findElementByXpath("./a/div[2]/div[1]/div[1]//b")
            if int(imageNum) >= minimal_photo_count:
                item.findElementByXpath("./a")
                link_info = item.getAttribute("href")
                self.scraping(link_info)
        except Exception as e:
            print(e)
            pass
        try:
            items = self.__exWaitS().until(
                ec.presence_of_all_elements_located((By.ID, "cBox-body cBox-body--resultitem dealerAd")),
                message="timeout trying to find items",
            )
            for item in items:
                imageNum = item.findElementByXpath("./a/div[2]/div[1]/div[1]//b")
                if int(imageNum) >= minimal_photo_count:
                    item.findElementByXpath("./a")
                    link_info = item.getAttribute("href")
                    self.scraping(link_info)
        except Exception as e:
            print(e)
            pass
        
    
    def scraping(self, link_url=""):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(link_url)
        time.sleep(100)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
            
if __name__ == "__main__":

    suchenMobileDe = SuchenMobileDe()
    suchenMobileDe.login()
    time.sleep(15)
    suchenMobileDe.start()