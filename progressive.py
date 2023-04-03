import csv
import logging
import pathlib
import random
import string
import time
import traceback
import sys

import dateutil.parser
import pandas as pd
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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


def get_random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "aol.com", "msn.com", "comcast.net"]
    size = random.randint(4, 8)
    domain = random.choice(domains)
    user_name = random_string(size)

    return f"{user_name}@{domain}"


class ProgressiveParser(Parser):
    def __init__(self, use_proxy=False, proxy_list=None):
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list
        self.driver = None
        self.fctbrowser = fctselenuim(
            type="chrome", use_proxy=self.use_proxy, proxy=self.proxy_list)  # mobile, chrome, firefox
        self.base_url = 'https://www.progressive.com/'

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

        try:
            zip_formatted = str(zip).split("-")[0]
            dob_formatted = dateutil.parser.parse(dob).strftime("%m-%d-%Y")
            image_name = f'/app/cache/progressive-{zip_formatted}-{firstname}-{lastname}.png'

            str1 = ''
            for _ in range(2):
                self.fctbrowser.open()
                str1 = self.fctbrowser.get(self.base_url, delay=5)
                self.driver = self.fctbrowser.driver
                str1 = self.driver.execute_script(
                    "return document.getElementsByTagName('html')[0].innerHTML"
                )
                if 'access denied' in str1.lower():
                    self.fctbrowser.close()
                else:
                    break

            page_exist = True
            if str1:
                try:
                    try:
                        class1 = '//div[@class="acsClassicInner"]//a[@aria-label="No, thanks"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).click()
                            time.sleep(random.randint(5, 10))
                    except:
                        ''

                    try:
                        class1 = '//a[@data-qs-product="AU"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).click()
                            time.sleep(random.randint(5, 10))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    try:
                        class1 = '//input[@id="zipCode_overlay"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.click()
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            elem.send_keys(zip_formatted)
                            time.sleep(random.randint(2, 5))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    try:
                        class1 = '//input[@id="qsButton_overlay"]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).click()
                            time.sleep(random.randint(30, 40))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    try:
                        class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_FirstName"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.click()
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            elem.send_keys(firstname)
                            time.sleep(random.randint(2, 5))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    try:
                        class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_LastName"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.click()
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            elem.send_keys(lastname)
                            time.sleep(random.randint(2, 5))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    try:
                        class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_DateOfBirth"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.click()
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            elem.send_keys(dob_formatted)
                            time.sleep(random.randint(3, 5))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    # try:
                    #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    #     time.sleep(random.randint(5, 10))
                    # except:
                    #     logging.error(traceback.format_exc())


                    # try:
                    #     class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_City"]'
                    #     if check_exists_by_xpath(class1, self.driver):
                    #         elem = self.driver.find_element(By.XPATH, class1)
                    #         elem.send_keys(Keys.CONTROL, 'a')
                    #         elem.send_keys(Keys.DELETE)
                    #         elem.send_keys(city)
                    #         time.sleep(1)
                    # except:
                    #     ''

                    try:
                        class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_MailingAddress"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            time.sleep(3)
                            elem.send_keys(address)
                            time.sleep(2)
                    except:
                        ''

                    try:
                        class1 = '//input[@id="NameAndAddressEdit_embedded_questions_list_City"]'
                        if check_exists_by_xpath(class1, self.driver):
                            elem = self.driver.find_element(By.XPATH, class1)
                            elem.send_keys(Keys.CONTROL, 'a')
                            elem.send_keys(Keys.DELETE)
                            time.sleep(0.5)
                            elem.send_keys(city)
                            time.sleep(1)
                    except:
                        ''

                    try:
                        class1 = '//button[contains(text(), "start my quote")]'
                        if check_exists_by_xpath(class1, self.driver):
                            self.driver.find_element(By.XPATH, class1).click()
                            time.sleep(random.randint(20, 30))
                        else:
                            page_exist = False
                    except:
                        page_exist = False

                    if page_exist:
                        # time.sleep(random.randint(5, 10))
                        str1 = self.driver.execute_script(
                            "return document.getElementsByTagName('html')[0].innerHTML"
                        )
                        html1 = Selector(text=str1)
                        parse_result = self.parse_page(
                            html1,
                            image_name,
                        )
                    else:
                        pass

                except:
                    self.driver.save_screenshot(image_name)
                    logging.error(traceback.format_exc())

            self.fctbrowser.close()

        except Exception as e:
            print(e)
            self.driver.save_screenshot(image_name)
            logging.error(traceback.format_exc())

        return parse_result

    def parse_page(
        self,
        html1,
        img,
    ) -> ParseResult:
        parse_result = ParseResult()

        errs = self.driver.find_elements(By.CLASS_NAME, 'alert-message-text')
        if len(errs) > 0:
            self.driver.save_screenshot(img)
            raise Exception(str(errs[0].text))

        car1 = car2 = car3 = car4 = car5 = car6 = car7 = car8 = car9 = car10 = ""
        try:
            car1 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[1]',
                html1)
            car2 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[2]',
                html1)
            car3 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[3]',
                html1)
            car4 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[4]',
                html1)
            car5 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[5]',
                html1)
            car6 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[6]',
                html1)
            car7 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[7]',
                html1)
            car8 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[8]',
                html1)
            car9 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[9]',
                html1)
            car10 = parse_field(
                '(//div[@class="content"]//div[contains(@class, "questions")]//question[contains(@class, "hvd-vehicle")]//*//question-label//label//span[contains(@class, "dynamic-content")])[10]',
                html1)
            # //*[@id="edac6a74-4606-4c5c-b162-511225ffbb9a"]/span

            # //*[@id="Year"]/span
            # /html/body/app-root/form/main/vehicle-all/vehicles-layout/interview-layout-template/div[1]/div/div/section/child-outlet-backend-scope/sliding-child-router-outlet/vehicle-details/small-layout-child-template/div/div/vehicle-shared-ymm-questions/div/div/question[1]/span/question-label/label/span/span
            cars = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10]
            # removes empty values
            cars = [car for car in cars if car]
            parse_result.cars = cars
            parse_result.has_car = True if car1 else False
            # Mark the result as valid, since no error occurred during parsing/crawling
            parse_result.valid = True
        except:
            self.driver.save_screenshot(img)
            logging.error(traceback.format_exc())

        return parse_result
