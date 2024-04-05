import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class NSEDataParser:
    def __init__(self, options):
        self.__driver = webdriver.Chrome(options)
        self.__wait = WebDriverWait(self.__driver, 10)

    def navigate_to_pre_open_market(self):
        self.__driver.get('https://www.nseindia.com')
        market_data_button = self.__wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="link_2"]')))
        ActionChains(self.__driver).move_to_element(market_data_button).perform()
        pre_open_market_button = self.__wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="main_navbar'
                                                                                               '"]/ul/li[3]/div/div['
                                                                                               '1]/div/div[1]/ul/li['
                                                                                               '1]/a')))
        pre_open_market_button.click()

    def parse_pre_open_market_data(self):
        self.waiting_until_data_update()

        self.change_category_to_all()
        data = []
        table_rows = self.__wait.until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="livePreTable"]'
                                                                                      '/tbody/tr')))
        table_rows.pop()
        for index, row in enumerate(table_rows, start=1):
            columns = row.find_elements(By.TAG_NAME, 'td')
            name = columns[1].find_element(By.TAG_NAME, 'a').text.strip()
            price = columns[6].text.strip()
            data.append([name, price])
            if index % 10 == 0:
                print(f'Получено {index} / {len(table_rows)} строк данных')
        print(f'Получение данных завершено')
        return data

    def change_category_to_all(self):
        self.change_selector_to('//*[@id="sel-Pre-Open-Market"]', 'ALL')

        self.waiting_until_data_update()

    def execute_user_scenario(self):
        home_button = self.__wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="link_0"]')))
        home_button.click()
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        self.__driver.execute_script("window.scrollTo(document.body.scrollHeight, 55);")

        nifty_bank_label = self.__wait.until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="tabList_NIFTYBANK"]')))
        nifty_bank_label.click()

        self.__driver.execute_script("window.scrollTo(55, 500);")

        view_all_button = self.__wait.until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="tab4_gainers_loosers"]/div[3]/a')))

        view_all_button.click()

        third_link_of_table = self.__wait.until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="equityStockTable"]/tbody/tr[3]/td[1]/a')))
        third_link_of_table.click()
        time.sleep(8)

    def change_selector_to(self, x_path, value):
        selector = self.__wait.until(ec.visibility_of_element_located((By.XPATH, x_path)))
        select = Select(selector)
        select.select_by_value(value)

    def waiting_until_data_update(self):
        self.__wait.until_not(ec.visibility_of_element_located((By.XPATH, '//*[@id="livePreTable"]/tbody/tr[2]/td[1]')))
        self.__wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="livePreTable"]/tbody/tr[2]/td[1]')))

    def close_driver(self):
        self.__driver.quit()
