# Импорт библиотек
# Importing libraries

import logging

import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def logging_work():
    """
    Настройки для логгирования скрипта
    Script logging settings
    """

    py_logger = logging.getLogger(__name__)
    py_logger.setLevel(logging.INFO)

    py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
    py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

    py_logger.info(f"Начало логгироваия {__name__}")

    return py_logger


def read_json_inn_com(logger):
    """
    Функция для получения инн компаний из csv-файла
    Function to get company TIN from csv file
    :return: inn_list - список инн компаний (list of inn companies)
    """

    logger.info(f'Start reading file from inn')
    try:

        path_csv = r"inn_org\inn_org.csv"
        with open(path_csv, 'r', encoding='utf-8-sig') as inn_csv:
            inn_list = list(map(lambda x: x.rstrip(), inn_csv.readlines()))

        logger.info(f'File {path_csv} read successfully')
        return inn_list

    except Exception as Error_read:
        logger.exception(f'Error while reading file. {Error_read}')
        return False


def work_selenium(logger, inn_list):
    try:
        logger.info(f'Driver setup and site connection')

        path_driver = r'Drivers\chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=path_driver)

        logger.info(f'Connection succeeded')

    except Exception as Error_connect:
        logger.exception(f'Error connecting to site. {Error_connect}')
        return False

    try:
        logger.info(f'Getting started with the site')
        driver.get('https://www.gosuslugi.ru/itorgs')
        delay = 6  # seconds
        try:
            for i in inn_list:
                elem_search = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@class='search-input ng-untouched ng-pristine ng-valid']")))
                elem_search.send_keys(i)
                elem_search.send_keys(Keys.RETURN)
                elem_search = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@class='link-plain small']")))
                elem_search.click()

            time.sleep(10)
        except TimeoutException:
            print("Loading took too much time!")

        logger.info(f'End of the site')

    except Exception as Error_work_site:
        logger.exception(f'Error while working with the site. {Error_work_site}')
        return False


if __name__ == '__main__':
    logger = logging_work()
    inn_list = read_json_inn_com(logger)
    work_selenium(logger, inn_list)
