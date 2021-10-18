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
        return WebDriverWait(self.driver, 10)
        
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
        try:
            acceptBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "mde-consent-accept-btn")),
                message="timeout trying to find accept button",
            )
            acceptBtn.click()
        except Exception as e:
            print(e)
            pass
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
            icon = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='save-search-tutorial']/span")),
                message="timeout trying to find icon",
            )
            icon.click()
        except Exception as e:
            print(e)
            pass
        while 1:
            try:
                topResult = self.__exWaitS().until(
                    ec.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[1]/div[3]/div[4]/div[2]/div[2]/div[4]")),
                    message="timeout trying to find top result item",
                )
                imageNum = topResult.find_elements_by_xpath("./a/div[2]/div[1]/div[1]/div//b")
                image_count_item = imageNum[0]
                if len(imageNum) > 1:
                    image_count_item = imageNum[1]
                print(f"-------------> {image_count_item.text}")
                if int(image_count_item.text) >= minimal_photo_count:
                    topResult_link = topResult.find_element_by_xpath("./a")
                    link_info = topResult_link.get_attribute("href")
                    self.scraping(link_info)
            except Exception as e:
                print(e)
                pass
            try:
                items = self.__exWaitS().until(
                    ec.presence_of_all_elements_located((By.XPATH, "/html/body/div[4]/div[1]/div[3]/div[4]/div[2]/div[2]/div[@class='cBox-body cBox-body--resultitem dealerAd']")),
                    message="timeout trying to find items",
                )
                for item in items:
                    imageNum = item.find_element_by_xpath("./a/div/div[1]/div/div/span[2]/b")
                    print(f"--------------> {imageNum.text}")
                    if int(imageNum.text) >= minimal_photo_count:
                        item_link = item.find_element_by_xpath("./a")
                        link_info = item_link.get_attribute("href")
                        self.scraping(link_info)
            except Exception as e:
                print(e)
                pass
            try:
                page_forward_btn = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "page-forward")),
                    message="timeout trying to find page forward button",
                )
                page_forward_btn.click()
            except Exception as e:
                print("-------------> Page Forward Button doesn't exist")
                break
        print("----------------> Scraping End")        
        
    def scraping(self, link_url=""):
        main_window= self.driver.current_window_handle
        self.driver.execute_script('window.open(arguments[0]);', link_url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        title = self.__exWaitS().until(
            ec.presence_of_element_located((By.ID, "ad-title")),
            message="timeout trying to find title",
        ).text
        self.driver.close()
        self.driver.switch_to.window(main_window)

if __name__ == "__main__":
    suchenMobileDe = SuchenMobileDe()
    suchenMobileDe.login()
    time.sleep(15)
    suchenMobileDe.start()