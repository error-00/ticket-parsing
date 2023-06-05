from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class Ticket:

    def __init__(self):
        self.place_of_departure = 'New York'
        self.destination = 'Los Angeles'
        self.date = '06/01/2023'
        self.passengers_count = 1

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def info_input(self):
        self.driver.get('https://www.aa.com/booking/find-flights?tripType=roundTrip#oneway')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ui-id-4']")))

        self.driver.find_element(By.XPATH, "//*[@id='ui-id-4']").click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='segments0.origin']")))

        # enter Place Of Departure
        departure_input = self.driver.find_element(By.XPATH, "//input[@id='segments0.origin']")
        try:
            departure_input.send_keys(self.place_of_departure)
            time.sleep(2)
            departure_input.send_keys(Keys.BACKSPACE)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ui-id-7']/li[1]")))
            self.driver.find_element(By.XPATH, "//*[@id='ui-id-7']/li[1]").click()
        except NoSuchElementException:
            departure_input.send_keys(self.place_of_departure[-1])

        # enter Destination
        destination_input = self.driver.find_element(By.XPATH, "//input[@id='segments0.destination']")
        try:
            destination_input.send_keys(self.destination)
            time.sleep(2)
            destination_input.send_keys(Keys.BACKSPACE)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ui-id-8']/li[1]")))
            self.driver.find_element(By.XPATH, "//*[@id='ui-id-8']/li[1]").click()
        except NoSuchElementException:
            destination_input.send_keys(self.destination[-1])

        # enter Date
        self.driver.find_element(By.XPATH, "//input[@id='segments0.travelDate']").send_keys(self.date)

        # enter A number of passengers
        self.driver.find_element(By.XPATH,
                                 f"//select[@id='passengerCount']/option[{self.passengers_count}]").click()

        # choose airline
        self.driver.find_element(By.XPATH, "//*[@id='airline']").click()
        self.driver.find_element(By.XPATH, "//*[@id='airline']/option[2]").click()

        self.driver.find_element(By.XPATH, "//button[@id='flightSearchSubmitBtn']").click()

        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, "//*[@id='aa-footer']")))

    def get_info(self):
        try:
            tickets_list = self.driver.find_elements(By.XPATH, "//div[@class='grid-x grid-padding-x ng-star-inserted']")
            num = 0
            for ticket in tickets_list:
                try:
                    city_code_1, *departure_time = ticket.find_element(By.XPATH,
                                                                       ".//div[@class='cell large-3 origin']").text.strip().split()
                except NoSuchElementException:
                    city_code_1, departure_time = None, None

                try:
                    city_code_2, *destination_time = ticket.find_element(By.XPATH,
                                                                         ".//div[@class='cell large-3 destination']").text.strip().split()
                except NoSuchElementException:
                    city_code_2, destination_time = None, None

                try:
                    duration = ticket.find_element(By.XPATH, ".//div[@class='duration']").text.strip()
                except NoSuchElementException:
                    duration = None

                try:
                    aircraft = ticket.find_element(By.XPATH,
                                                   ".//span[@class='connecting-flt-details aircraft-name']").text.strip()
                except NoSuchElementException:
                    aircraft = None

                try:
                    # basic_economy = ticket.find_element(By.XPATH,
                    #                                     ".//div[@class='cell auto pad-left-xxs pad-right-xxs ng-star-inserted'][1]").text.strip().split()
                    basic_economy = ticket.find_element(By.XPATH,
                                                        f"//button[@id='flight{num}-product0']/app-choose-flights-price-desktop/span").text.strip()
                except NoSuchElementException:
                    basic_economy = None

                try:
                    main_cabin = ticket.find_element(By.XPATH,
                                                     f"//button[@id='flight{num}-product1']/app-choose-flights-price-desktop/span").text.strip()
                except NoSuchElementException:
                    main_cabin = None

                try:
                    business = ticket.find_element(By.XPATH,
                                                   f"//button[@id='flight{num}-product2']/app-choose-flights-price-desktop/span").text.strip()
                except NoSuchElementException:
                    business = None

                try:
                    first = ticket.find_element(By.XPATH,
                                                f"//button[@id='flight{num}-product3']/app-choose-flights-price-desktop/span").text.strip()
                except NoSuchElementException:
                    first = None

                print('#########################')
                print(
                    f'({city_code_1}) {" ".join(departure_time)} -> ({city_code_2}) {" ".join(destination_time)} \nDuration: {duration}\n\t{aircraft}\nBasic Economy: {basic_economy}\nMain Cabin: {main_cabin}\nBusiness: {business}\nFirst: {first}\n\n')

                num += 1

        except NoSuchElementException:
            print("Билеты не найдены")

        self.driver.quit()


T = Ticket()

T.info_input()
T.get_info()
