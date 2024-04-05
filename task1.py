import csv
from selenium.webdriver.chrome.options import Options
from classes.nse_data_parser import NSEDataParser


def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Final Price'])
        writer.writerows(data)


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.ignore_local_proxy_environment_variables()

    parser = NSEDataParser(options=chrome_options)
    try:
        parser.navigate_to_pre_open_market()

        pre_open_market_data = parser.parse_pre_open_market_data()

        write_to_csv(pre_open_market_data, 'NSE.csv')

        parser.execute_user_scenario()
    finally:
        parser.close_driver()
