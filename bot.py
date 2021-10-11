from datetime import date, datetime, timedelta
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

from log import Log
from xpath import *
import pandas as pd

class Nextdoor():

    def __init__(self):
        self.user_mail = ""
        self.user_pswd = ""
        self.date = ""
        self.time = ""
        self.post_category =  ""
        self.post_subject = ""
        self.post_message = ""
        self.read_csv()
        self.log = Log()
        self.site_url = "https://nextdoor.com/"
        self.newsfeed_url = "https://nextdoor.co.uk/news_feed/"
        options = Options()
        options.add_argument("--window-size=1920,1200")
        self.driver = Chrome(options=options, executable_path="chromedriver.exe")
        
    def read_csv(self):
        df = pd.read_csv("next_door.csv")
        input_data = df.iloc[0, :].values.tolist()
        self.user_mail = input_data[0]
        self.user_pswd = input_data[1]
        self.date = input_data[2]
        self.time = input_data[3]
        self.post_category = input_data[4]
        self.post_subject = input_data[5]
        self.post_message = input_data[6]
        
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
    
    def login(self):
        try:
            self.driver.get(self.site_url)
            login_btn1 = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, user["user-login-btn1"])),
                message="timeout trying to find the login button on the nextdoor page",
            )
            self._click(login_btn1, "Click the login button on the nextdoor page")
            
            emailField = self.__exWaitS().until(
                ec.presence_of_element_located(
                    (By.XPATH, user["user-email-field"])
                ),
                message="timeout trying to find email field",
            )
            emailField.send_keys(self.user_mail)

            pswdField = self.__exWaitS().until(
                ec.presence_of_element_located(
                    (By.XPATH, user["user-password-field"])
                ),
                message="timeout trying to find password field",
            )
            pswdField.send_keys(self.user_pswd)
            
            login_btn2 = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, user["user-login-btn2"])),
                message="timeout trying to find the login button on the login page",
            )
            
            self._click(login_btn2, "Click the login button on the login page")
            self._waiting(10, "Wait for newsfeed page to appear")
            
            self.post()
                
        except Exception as e:
            print(e)
            
    def categories_to_numbers(self, argument):
        switcher = {
            "Ask a neighbour": "1",
            "Finds (For Sale & Free)": "2",
            "Documents": "3",
            "Safety": "4",
            "Lost and Found": "5",
            "General": "6",
        }
    
        return switcher.get(argument, 1)
    
    def post(self):
        postField = self.__exWaitS().until(
            ec.presence_of_element_located((By.XPATH, home['post-field'])),
            message="timeout trying to find post field button",
        )
        self._click(postField, "Click the post field button on the newsfeed page")

        postCategoryBtn = self.__exWaitS().until(
            ec.presence_of_element_located((By.XPATH, home['post-categorybtn'])),
            message="timeout trying to find post category button",
        )
        self._click(postCategoryBtn, "Click the category button on the newsfeed page")
        
        categoryNumber = self.categories_to_numbers(self.post_category)
        postCategory = self.__exWaitS().until(
            ec.presence_of_element_located((By.XPATH, home['post-category'+categoryNumber])),
            message="timeout trying to find post category",
        )
        self._click(postCategory, "Click the category on the newsfeed page")
        
        postSubject = self.__exWaitS().until(
            ec.presence_of_element_located(
                (By.XPATH, home["post-subject"])
            ),
            message="timeout trying to find subject ",
        )
        postSubject.send_keys(self.post_subject)

        postMessage = self.__exWaitS().until(
            ec.presence_of_element_located(
                (By.XPATH, home["post-message"])
            ),
            message="timeout trying to find message textarea",
        )
        postMessage.send_keys(self.post_message)

        postBtn = self.__exWaitS().until(
            ec.presence_of_element_located(
                (By.XPATH, home["post-btn"])
            ),
            message="timeout trying to find Post button",
        )
        
        targetTime = datetime.strptime(self.date + " " + self.time, "%d/%m/%Y %I:%M%p")
        sleepingTime = (targetTime - datetime.now()).total_seconds()
        sleepingTime = sleepingTime if sleepingTime > 0 else 0
        self._waiting(sleepingTime, "Wait until target time")
        
        self._click(postBtn, "Click the Post button on the newsfeed page")
        self._waiting(5, "Wait for the new post to appear")
        self.driver.quit()
        
if __name__ == "__main__":

    nextdoor = Nextdoor()
    nextdoor.login()