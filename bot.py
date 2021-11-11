from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
# from seleniumrequests import Chrome
from log import Log
from xpath import *
import time
import os
import requests
from configparser import ConfigParser

class SuchenMobileDe():
    def __init__(self):
        self.log = Log()
        self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0"
        self.s = requests.Session()
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_extension("adblock_extension_4_33_0_0.crx")
        self.driver = webdriver.Chrome(executable_path='chromedriver95.0.4638.69.exe', options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.main_window = self.driver.current_window_handle
        self.ad_num = 0
        
        self.vehicle = self.configuration()[0]
        self.price_from = self.configuration()[1]
        self.price_to = self.configuration()[2]
        self.registration_from = self.configuration()[3]
        self.registration_to = self.configuration()[4]
        self.kilometer_from = self.configuration()[5]
        self.kilometer_to = self.configuration()[6]
        self.minimal_photo_count = self.configuration()[7]
        self.provider = self.configuration()[8]
        self.directory_path = self.configuration()[9]
        self.location = self.configuration()[10]
        
    def configuration(self):
        config = ConfigParser()
        config.readfp(open(f"input.cfg"))
        cars = config.get("vehicle_type", "cars")
        motorcycles = config.get("vehicle_type", "motorcycles")        
        price_from = config.get("values", "price_from")
        price_to = config.get("values", "price_to")
        registration_from = config.get("values", "registration_from")
        registration_to = config.get("values", "registration_to")
        kilometer_from = config.get("values", "kilometer_from")
        kilometer_to = config.get("values", "kilometer_to")
        minimal_photo_count = config.get("values", "minimal_photo_count")
        any = config.get("provider", "any")
        Private_provider = config.get("provider", "Private_provider")
        Dealers = config.get("provider", "Dealers")
        Company_vehicles = config.get("provider", "Company_vehicles")
        directory_path = config.get("directory_path", "directory_path")
        location = config.get("values", "location")
        
        vehicle = "cars"
        if motorcycles is not None and motorcycles == "1":
            vehicle = "motorcycles"
        if price_from is not None and price_from.isdigit() and int(price_from) > 0:
            price_from = int(price_from)
        else: price_from = -1
        if price_to is not None and price_to.isdigit() and int(price_to) > 0:
            price_to = int(price_to)
        else: price_to = -1
        if registration_from is not None and registration_from.isdigit() and int(registration_from) > 0:
            registration_from = int(registration_from)
        else: registration_from = -1
        if registration_to is not None and registration_to.isdigit() and int(registration_to) > 0:
            registration_to = int(registration_to)
        else: registration_to = -1
        if kilometer_from is not None and kilometer_from.isdigit() and int(kilometer_from) > 0:
            kilometer_from = int(kilometer_from)
        else: kilometer_from = -1
        if kilometer_to is not None and kilometer_to.isdigit() and int(kilometer_to) > 0:
            kilometer_to = int(kilometer_to)
        else: kilometer_to = -1
        if minimal_photo_count is not None and minimal_photo_count.isdigit() and int(minimal_photo_count) > 0:
            minimal_photo_count = int(minimal_photo_count)
        else: minimal_photo_count = 0
        provider = "any"
        if Private_provider is not None and Private_provider == "1":
            provider = "Private provider"
        elif Dealers is not None and Dealers == "1":
            provider = "Dealers"
        elif Company_vehicles is not None and Company_vehicles == "1":
            provider = "Company vehicles"
        if directory_path is None:
            directory_path = "Results"
        if location is None:
            location = "Any"
            
        return (
            vehicle, 
            price_from, 
            price_to,
            registration_from, 
            registration_to, 
            kilometer_from, 
            kilometer_to, 
            minimal_photo_count, 
            provider, 
            directory_path,
            location,
        )

    def __exWaitS(self):
        # Implicit waiting functions
        return WebDriverWait(self.driver, 10)
        
    def _click(self, element, msg=" "):
        # This functions is to just click stuff
        self.log.write_log("bot", msg)
        self.driver.execute_script("arguments[0].click();", element)
        
    def _waiting(self, waitingTime, msg=" "):
        # Waiting for waitingTime seconds
        self.log.write_log("bot", msg)
        time.sleep(waitingTime)
        
    def __switch_tab(self):
        visible_windows = self.driver.window_handles

        for window in visible_windows:
            if window != self.main_window:
                self.driver.switch_to.window(window)
                self.driver.close()
                self.driver.switch_to.window(self.main_window)
    
    def beauty(self, first="", second=""):
        if len(first) < 30:
            return first + ' ' * (30 - len(first)) + second
        return first + ' ' + second
    
    def login(self, vehicle_type="cars", price_from=-1, price_to=-1, registration_from=-1, registration_to=-1, kilometer_from=-1, kilometer_to=-1, provider="any", location="Any"):
        self.log.write_log("bot", vehicle_type)
        if vehicle_type == "cars":
            self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0"
        elif vehicle_type == "motorcycles":
            self.site_url = "https://suchen.mobile.de/fahrzeuge/search.html?vc=Motorbike"
        self.driver.get(self.site_url)
        time.sleep(5)
        self.__switch_tab()
        try:
            acceptBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "mde-consent-accept-btn")),
                message="timeout trying to find accept button",
            )
            self._click(acceptBtn, "Clicking accept button")
        except Exception as e:
            print(e)
            pass
        try:
            time.sleep(2)
            acceptBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='mde-consent-modal-container']/div/div[2]/button")),
                message="timeout trying to find modal container button",
            )
            self._click(acceptBtn, "Clicking modal container button")
        except Exception as e:
            print(e)
            pass
        if price_from != -1:
            try:
                time.sleep(2)
                minPrice = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minPrice")),
                    message="timeout trying to find min price input",
                )
                minPrice.send_keys(price_from)
                self.log.write_log("bot", "Price-from field pass")
            except Exception as e:
                print(e)
                pass
        if price_to != -1:
            try:
                time.sleep(2)
                maxPrice = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxPrice")),
                    message="timeout trying to find max price input",
                )
                maxPrice.send_keys(price_to)
                self.log.write_log("bot", "Price-to field pass")
            except Exception as e:
                print(e)
                pass
        if registration_from != -1:
            try:
                time.sleep(2)
                minFirstRegistrationDate = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minFirstRegistrationDate")),
                    message="timeout trying to find min registration input",
                )
                minFirstRegistrationDate.send_keys(registration_from)
                self.log.write_log("bot", "registration-from field pass")
            except Exception as e:
                print(e)
                pass
        if registration_to != -1:
            try:
                time.sleep(2)
                maxFirstRegistrationDate = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxFirstRegistrationDate")),
                    message="timeout trying to find max registration input",
                )
                maxFirstRegistrationDate.send_keys(registration_to)
                self.log.write_log("bot", "registration-to field pass")
            except Exception as e:
                print(e)
                pass
        if kilometer_from != -1:
            try:
                time.sleep(2)
                minMileage = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "minMileage")),
                    message="timeout trying to find min kilometer input",
                )
                minMileage.send_keys(kilometer_from)
                self.log.write_log("bot", "kilometer-from field pass")
            except Exception as e:
                print(e)
                pass
        if kilometer_to != -1:
            try:
                time.sleep(2)
                maxMileage = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "maxMileage")),
                    message="timeout trying to find max kilometer input",
                )
                maxMileage.send_keys(kilometer_to)
                self.log.write_log("bot", "kilometer-to field pass")
            except Exception as e:
                print(e)
                pass
        self.log.write_log("bot", "Vehicle type: "+provider)
        if provider == "any":
            try:
                time.sleep(2)
                anyRadio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation--ds")),
                    message="timeout trying to find any radio",
                )
                self._click(anyRadio, "Any radio button click")
            except Exception as e:
                print(e)
                pass
        elif provider == "Private provider":
            try:
                time.sleep(2)
                private_provider_radio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_FSBO_ADS-ds")),
                    message="timeout trying to find private provider radio",
                )
                self._click(private_provider_radio, "private_provider radio button click")
            except Exception as e:
                print(e)
                pass
        elif provider == "Dealers":
            try:
                time.sleep(2)
                dealerRadio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_DEALER_ADS-ds")),
                    message="timeout trying to find dealer radio",
                )
                self._click(dealerRadio, "dealer radio button click")
            except Exception as e:
                print(e)
                pass
        elif provider == "Company vehicles":
            try:
                time.sleep(2)
                company_vehicle_radio = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "adLimitation-ONLY_COMMERCIAL_FSBO_ADS-ds")),
                    message="timeout trying to find company vehicle radio",
                )
                self._click(company_vehicle_radio, "company_vehicle radio button click")
            except Exception as e:
                print(e)
                pass
        self.log.write_log("bot", "Location: "+location)
        if location != "Any":
            if location == "Germany" or location == "germany" or location == "Deutschland":
                try:
                    time.sleep(2)
                    countryBtn = self.__exWaitS().until(
                        ec.presence_of_element_located((By.ID, "ambit-search-country")),
                        message="timeout trying to find country button",
                    )
                    self._click(countryBtn, "Country button click")
                    countryBtn.find_element_by_xpath("./optgroup[1]/option[2]").click()
                except Exception as e:
                    print(e)
                    pass
            else:
                try:
                    time.sleep(2)
                    countryBtn = self.__exWaitS().until(
                        ec.presence_of_element_located((By.ID, "ambit-search-country")),
                        message="timeout trying to find country button",
                    )
                    self._click(countryBtn, "Contry dropdown button click")
                    for option in countryBtn.find_elements_by_xpath("./optgroup[2]/option"):
                        if location == option.text:
                            option.click()
                            break
                except Exception as e:
                    print(e)
                    pass
        try:
            time.sleep(3)
            searchBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "dsp-upper-search-btn")),
                message="timeout trying to find offer button",
            )
            self.log.write_log("bot", "Clicking Search button")
            self.log.write_log("bot", "Total Ads Count: "+searchBtn.find_element_by_xpath("./span").text)
            self._click(searchBtn, f"Search button click")
        except Exception as e:
            print(e)
            pass
            
    def start(self, minimal_photo_count=0, directory_path="Results"):
        try:
            icon = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='save-search-tutorial']/span")),
                message="timeout trying to find icon",
            )
            self._click(icon, "Save search button click")
        except Exception as e:
            print(e)
            self.log.write_log("bot", "Save search button clicking exception")
            pass
        page_num = 0
        while 1:
            page_num += 1
            print()
            self.log.write_log("bot", f"{page_num}page scraping start")
            try:
                results = self.__exWaitS().until(
                    ec.presence_of_all_elements_located((By.XPATH, "//div[@class='cBox cBox--content cBox--resultList']/div")),
                    message="timeout trying to find all results",
                )
                for result in results:
                    if "cBox-body cBox-body--topResultitem" in result.get_attribute("class"):
                        topResult = result
                        imageNum = topResult.find_elements_by_xpath("./a/div[2]/div[1]/div[1]/div//b")
                        image_count_item = imageNum[0]
                        if len(imageNum) > 1:
                            image_count_item = imageNum[1]
                        self.log.write_log("bot", f"Top image Count: {image_count_item.text}")
                        self.log.write_log("bot", f"Minimal image Count: {minimal_photo_count}")
                        if int(image_count_item.text) >= minimal_photo_count:
                            self.log.write_log("bot", "Top Ad scraping")
                            topResult_link = topResult.find_element_by_xpath("./a")
                            link_info = topResult_link.get_attribute("href")
                            self.scraping(link_info, directory_path)
                        
            except Exception as e:
                self.log.write_log("bot", "Top Ad scraping exception")
                pass
            try:
                items = self.__exWaitS().until(
                    ec.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='no-top']")),
                    message="timeout trying to find items",
                )
                for idx in range(len(items)):
                    try:
                        imageNum = items[idx].find_element_by_xpath("./a//b")
                        print()
                        self.log.write_log("bot", f"{page_num} page {idx+1} Ad image Count: {imageNum.text}")
                        self.log.write_log("bot", f"Minimal image Count: {minimal_photo_count}")
                        if int(imageNum.text) >= minimal_photo_count:
                            self.log.write_log("bot", f"{page_num} page {idx+1} Ad scraping")
                            item_link = items[idx].find_element_by_xpath("./a")
                            link_info = item_link.get_attribute("href")
                            self.scraping(link_info, directory_path)
                    except:
                        pass
            except Exception as e:
                self.log.write_log("bot", "Normal Ad scraping exception")
                pass
            try:
                page_forward_btn = self.__exWaitS().until(
                    ec.presence_of_element_located((By.ID, "page-forward")),
                    message="timeout trying to find page forward button",
                )
                self._click(page_forward_btn, f"{page_num} page forward button click")
            except Exception as e:
                self.log.write_log("bot", "Page Forward Button doesn't exist")
                break
        print()
        self.log.write_log("bot", f"Scraping end")
        
    def scraping(self, link_url="", directory_path="Results"):
        self.ad_num += 1
        self.log.write_log("bot", f"{self.ad_num} Ad scraping start")
        
        # try:
        #     response = self.s.get(link_url)
        #     print(response.text)
        # except:
        #     print("response exception")
        #     pass
        # time.sleep(1000)

        main_window= self.driver.current_window_handle
        self.driver.execute_script('window.open(arguments[0]);', link_url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            acceptBtn = self.__exWaitS().until(
                ec.presence_of_element_located((By.ID, "mde-consent-accept-btn")),
                message="timeout trying to find accept button",
            )
            self._click(acceptBtn, "Accept button click")
        except Exception as e:
            self.log.write_log("bot", "Accept button clickng exception")
            pass
        
        title = self.__exWaitS().until(
            ec.presence_of_element_located((By.ID, "ad-title")),
            message="timeout trying to find title",
        ).text
        self.log.write_log("bot", "Title scraping: "+title)
        if "Results" in directory_path:
            cwd = os.getcwd()
            directory_path = os.path.join(cwd, directory_path)
        if os.path.exists(directory_path):
            title1 = title.replace("*", "").replace("/", "").replace("\\", "").replace(":", "").replace("|", "").replace("?", "").replace("<", "").replace(">", "").replace("\"", "").replace("+", "").replace("-", "").replace(".", "").replace(",", "").replace("-", "")
            directory_path = os.path.join(directory_path, title1).strip()
            if not os.path.isdir(directory_path):
                os.mkdir(directory_path)
                self.log.write_log("bot", "Directory creating: "+directory_path)
        try:
            image_wrappers = self.__exWaitS().until(
                ec.presence_of_all_elements_located((By.XPATH, "//div[@id='fullscreen-overlay-image-gallery-container']/div/div[2]/div/div[2]/div")),
                message="timeout trying to find image wrapper",
            )
            index = 0
            for image_wrapper in image_wrappers:
                if image_wrapper.get_attribute("id").startswith("gallery-img"):
                    image_src = image_wrapper.find_element_by_xpath("./img").get_attribute("data-lazy")
                    index = index + 1
                    self.log.write_log("bot", f"{index} image scraping: {image_src}")
                    response = requests.get("https:"+image_src)
                    if response.status_code == 200:
                        with open(f"{directory_path}\\{index}.jpg","wb") as file:
                            file.write(response.content)
        except Exception as e:
            self.log.write_log("bot", "Images scraping exception")
            pass
        results = '<table>'
        results += '<tr><td>Title</td><td>'+title+'</td></tr>'
        try:
            address = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='top-dealer-info']/p[@id='seller-address']")),
                message="timeout trying to find address",
            ).text
            results += f'<tr><td>Address</td><td>{address}</td></tr>'
            self.log.write_log("bot", f"Address scraping: {address}")
        except Exception as e:
            self.log.write_log("bot", "Address scraping exception")
            pass
        try:
            price = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@id='td-box']/div[1]/div[2]/span[1]")),
                message="timeout trying to find price",
            ).text
            self.log.write_log("bot", f"Price scraping: {price}")
            results += '<tr><td>Price</td><td>'+price+'</td></tr>'
        except Exception as e:
            self.log.write_log("bot", "Price scraping exception")
            pass
        try:
            items = self.__exWaitS().until(
                ec.presence_of_all_elements_located((By.XPATH, "//div[@id='td-box']/div")),
                message="timeout trying to find the whole content",
            )
            for idx, item in enumerate(items):
                if idx > 0:
                    item_title = item.find_element_by_xpath(".//strong").text
                    item_content = item.find_element_by_xpath("./div[2]").text
                    results += '<tr><td>'+item_title+'</td><td>'+item_content+'</td></tr>'
                    self.log.write_log("bot", f"{item_title} scraping: {item_content}")
        except Exception as e:
            self.log.write_log("bot", "Each Item scraping exception")
            pass
        try:
            description =  self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, "//div[@class='cBox-body cBox-body--vehicledescription']/div/div")),
                message="timeout trying to find description",
            )
            results += '<tr></tr><tr><td colspan="2"><h3>Description</h3></td></tr>'
            results += f'<tr><td colspan="2">{description.text}</td></tr>'
            self.log.write_log("bot", f"description scraping")
        except Exception as e:
            self.log.write_log("bot", "Description scraping exception")
            pass
        results += '</table>'
        with open(f"{directory_path}\\results.html","wb") as file:
            file.write(results.encode('utf-8'))
        self.driver.close()
        self.driver.switch_to.window(main_window)

if __name__ == "__main__":
    suchenMobileDe = SuchenMobileDe()        
    suchenMobileDe.login(suchenMobileDe.vehicle, suchenMobileDe.price_from, suchenMobileDe.price_to, suchenMobileDe.registration_from, suchenMobileDe.registration_to, suchenMobileDe.kilometer_from, suchenMobileDe.kilometer_to, suchenMobileDe.provider, suchenMobileDe.location)
    time.sleep(3)
    suchenMobileDe.start(suchenMobileDe.minimal_photo_count, suchenMobileDe.directory_path)