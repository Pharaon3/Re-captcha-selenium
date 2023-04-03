import csv
import logging
import pathlib
import random
import time
import traceback
import string

import dateutil.parser
import pandas as pd
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import selenium.common.exceptions as exceptions
import sys

if sys.platform == 'win32':
    from fctcore import (
        Parser,
        ParseResult,
        check_exists_by_xpath,
        fctselenuim,
        parse_field,
        preg_repace,
    )

else:
    from crawler.fctcore import (
        Parser,
        ParseResult,
        check_exists_by_xpath,
        fctselenuim,
        parse_field,
        preg_repace,
    )
    
def random_string(size: int) -> str:
    return "".join((random.choice(string.ascii_letters.lower()) for _ in range(size)))


def generate_random_phone_number():
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def get_random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "msn.com", "comcast.net"]
    size = random.randint(4, 8)
    domain = random.choice(domains)
    user_name = random_string(size)

    return f"{user_name}@{domain}"

class TravelersParser(Parser):
    def __init__(self, use_proxy=False, proxy_list=None):
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.driver = None
        self.fctbrowser = fctselenuim(  type="chrome", use_proxy=self.use_proxy, proxy=self.proxy_list, use_defenders=True)
        self.base_url = "https://www.travelers.com/"
    
    def parse_site(
        self,
        firstname: str,
        lastname: str,
        address: str,
        city: str,
        state: str,
        zip: str,
        dob: str,
    ) -> ParseResult:
        parse_result = None
        if firstname == "":
            raise Exception("First name missing")
        if lastname == "":
            raise Exception("Last name missing")
        if dob == "":
            raise Exception("Date-of-birth missing")
        if address == "":
            raise Exception("Address name missing")
        no_auto_insurance = False
        
        try:
            zip_formatted = zip.split("-")[0]
            if len(zip_formatted) == 4:
                zip_formatted = '0' + zip_formatted
            dob_formatted = dateutil.parser.parse(dob).strftime("%m-%d-%Y")
            dob_formatted_month = dateutil.parser.parse(dob).strftime("%m")
            dob_formatted_day = dateutil.parser.parse(dob).strftime("%d")
            dob_formatted_year = dateutil.parser.parse(dob).strftime("%Y")
            image_name = f'/pics/travelers-{zip_formatted}-{firstname}-{lastname}.png'
            
            str1 = ''
            for _ in range(3):
                self.fctbrowser.open()
                self.driver = self.fctbrowser.driver
                str1 = self.fctbrowser.get(self.base_url, delay=5)
                str1 = self.driver.execute_script(
                    "return document.getElementsByTagName('html')[0].innerHTML"
                )
                time.sleep(random.randint(5, 10))
                if 'zip code' not in str1.lower():
                    self.fctbrowser.close()
                    time.sleep(random.randint(3, 5))
                else:
                    break
            
            page_exist = True
            if str1:
                try:
                    for i in range(3):
                        try:
                            class1 = '//*[@id="quote-zip-code"]'
                            if check_exists_by_xpath(class1, self.driver):
                                elem = self.driver.find_element(By.XPATH, class1)
                                elem.click()
                                elem.send_keys(Keys.CONTROL, "a")
                                elem.send_keys(Keys.DELETE)
                                elem.send_keys(zip_formatted)
                                time.sleep(random.randint(3, 5))
                            else:
                                page_exist = False
                        except:
                            page_exist = False

                        try:
                            class1 = '//*[@id="body-btn-get-quote"]'
                            if check_exists_by_xpath(class1, self.driver):
                                self.driver.find_element(By.XPATH, class1).click()
                                time.sleep(random.randint(15, 20))
                                self.driver = self.fctbrowser.driver
                                str2 = self.driver.execute_script(
                                    "return document.getElementsByTagName('html')[0].innerHTML"
                                )
                                if 'access denied' in str2.lower() or 'no internet' in str2.lower():
                                    self.fctbrowser.close()
                                    time.sleep(random.randint(3, 5))
                                    if i == 2:
                                        print("Error: max try number exceeded")
                                        page_exist = False
                                        return
                                    else:
                                        for _ in range(3):
                                            self.fctbrowser.open()
                                            str1 = self.fctbrowser.get(self.base_url, delay=5)
                                            self.driver = self.fctbrowser.driver
                                            str1 = self.driver.execute_script(
                                                "return document.getElementsByTagName('html')[0].innerHTML"
                                            )
                                            if 'zip code' not in str1.lower():
                                                self.fctbrowser.close()
                                                time.sleep(random.randint(3, 5))
                                            else:
                                                break
                                else:
                                    break
                            else:
                                page_exist = False
                        except:
                            page_exist = False
                       
                    try:
                        self.driver = self.fctbrowser.driver
                        str1 = self.driver.execute_script(
                            "return document.getElementsByTagName('html')[0].innerHTML"
                        )
                        if 'We do not currently write new auto insurance policies in your state' in str1:
                            print(f"Error: insurance not available for {state}")
                            no_auto_insurance = True
                            raise Exception()
                        if 'We are unable to quote you online' in str1:
                            print("Error: online quoting for this entry is not available")
                            no_auto_insurance = True
                            raise Exception()
                        if 'Please contact a local independent insurance agent' in str1:
                            print("Error: auto insurance coverage not available for this entry")
                            no_auto_insurance = True
                            raise Exception()
                    except:
                        page_exist = False
                        
                    try:
                        class1 = '//*[@id="continue"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).click()
                            time.sleep(random.randint(10, 15))
                    except:
                        page_exist = False
                        
                    try:
                        self.driver.execute_script("document.body.style.zoom = '50%'")
                        time.sleep(random.randint(1, 2))
                        class1 = '//*[@id="firstName"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(firstname)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                        
                    try:
                        class1 = '//*[@id="lastName"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(lastname)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="streetAddr1"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(address)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//select[@name="streetAddrCity"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            slc = Select(elem)
                            if len(slc.options) > 1:
                                class2 = f'//select[@name="streetAddrCity"]/option[2]'
                                elem = self.driver.find_element(By.XPATH, class2)
                                elem.click()
                                time.sleep(random.randint(2, 3))
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="radGenderMale"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.execute_script('document.getElementById("radGenderMale").checked = true;')
                            time.sleep(random.randint(2, 3))
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//select[@name="genderCd"]'
                        if check_exists_by_xpath(class1, self.driver):
                            class4 = f'//select[@name="genderCd"]/option[@value="M"]'
                            elem = self.driver.find_element(By.XPATH, class4)
                            elem.click()
                            time.sleep(random.randint(2, 3))
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="dobMonth"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(dob_formatted_month)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="dobDay"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(dob_formatted_day)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="dobYear"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(dob_formatted_year)
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="continue"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).send_keys(Keys.ENTER)
                            time.sleep(random.randint(10, 15))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="emailAddress"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(get_random_email())
                            time.sleep(random.randint(2, 3))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    try:
                        class1 = '//*[@id="continue"]'
                        if check_exists_by_xpath(class1, self.driver):
                            button = self.driver.find_element(By.XPATH, class1)
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(random.randint(10, 15))
                        else:
                            page_exist = False
                    except:
                        page_exist = False
                    
                    if page_exist:
                        time.sleep(random.randint(3, 5))
                        self.driver = self.fctbrowser.driver
                        str1 = self.driver.execute_script(
                            "return document.getElementsByTagName('html')[0].innerHTML"
                        )
                        html1 = Selector(text=str1)
                        parse_result = self.parse_page(
                            html1,
                            image_name,
                        )
                    else:
                        if not no_auto_insurance:
                            self.driver.save_screenshot(image_name)
                            print("failed to get data")
            
                except:
                    self.driver.save_screenshot(image_name)
                    logging.error(traceback.format_exc())
                    
            self.fctbrowser.close()
                    
        except:
            self.driver.save_screenshot(image_name)
            logging.error(traceback.format_exc())
        
        return parse_result
    
    def parse_page(
        self,
        html1,
        img,
    ):
        parse_result = ParseResult(is_customer=False, cars=[])
        car1 = car2 = car3 = car4 = car5 = car6 = car7 = car8 = car9 = car10 = ""
        try:
            car1 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[1]', html1)
            car2 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[2]', html1)
            car3 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[3]', html1)
            car4 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[4]', html1)
            car5 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[5]', html1)
            car6 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[6]', html1)
            car7 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[7]', html1)
            car8 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[8]', html1)
            car9 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[9]', html1)
            car10 = parse_field('//*[@id="vehicleSummary"]/div[2]/div[10]', html1)

            cars_old = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10]
            cars = []
            for car in cars_old:
                if car:
                    if 'Add a vehicle' in car:
                        continue
                    if car[-3:] == "Add":
                        car = car[:-3].strip()
                    cars.append(car)

            parse_result.has_car = True if cars else False
            parse_result.cars = cars

            parse_result.valid = True
            
            return parse_result

        except:
            self.driver.save_screenshot(img)
            logging.error(traceback.format_exc())