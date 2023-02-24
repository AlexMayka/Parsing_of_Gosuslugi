# Импорт библиотек
# Importing libraries

import logging
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def logging_work() -> logging:
    """
    Настройки для логгирования скрипта;
    Script logging settings;
    """

    py_logger = logging.getLogger(__name__)
    py_logger.setLevel(logging.INFO)

    py_handler = logging.FileHandler(r"log_for_work.log", mode='w')
    py_formatter = logging.Formatter("%(name)s %(asctime)s "
                                     "%(levelname)s %(message)s")

    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

    py_logger.info(f"Begin logging {__name__}")

    return py_logger


def read_csv_inn_com(logger: object = logging) -> list | bool:
    """
    Функция для получения инн компаний из csv-файла;
    Function to get company TIN from csv file;

    :return: inn_list: список инн компаний (list of inn companies);
    """

    logger.info('Start reading file from inn')
    try:

        path_csv = r"inn_org\inn_org.csv"
        with open(path_csv, 'r', encoding='utf-8-sig') as inn_csv:
            inn_list = list(map(lambda x: x.rstrip(), inn_csv.readlines()))

        logger.info(f'File {path_csv} read successfully')
        return inn_list

    except Exception as Error_read:
        logger.exception(f'Error while reading file. {Error_read}')
        return False


def input_data(driver: object = webdriver, delay=10, inn: object = int):
    """
    Функция для ввода информации в форму поиска
    Function for entering information into the search form

    :param driver: элемент класса браузера (browser class element);
    :param delay: время задержки для поиска (delay time for search)
    :param inn: инн компании (inn company)
    """
    try:
        logger.info(f'Data_entry_{inn}')
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='search-input ng-untouched ng-pristine ng-valid']")))
        elem_search_string.clear()
        elem_search_string.send_keys(inn)
        elem_search_string.send_keys(Keys.ENTER)
        logger.info(f'Successful_search_{inn}')
    except Exception as exp:
        logger.exception(f'Data entry error: {exp}')


def check_response(driver: object = webdriver, df: object = pd.DataFrame, inn: object = int) -> pd.DataFrame:
    """
    Функция проверки и записи в df;
    The function of checking and writing to df;
    @param driver: элемент класса браузера (browser class element);
    @param df: Data Frame для записи результатов (Data Frame for recording results);
    @param inn: инн компании (inn company)
    @return: Data Frame с новыми данными ( Data Frame with new data);
    """

    delay = 2
    logger.info(f'Start_check_inn - {inn}')
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//img[@class='img-ok']")
            )
        )
        elem_text_response = driver.find_element(
            By.XPATH,
            "//div[@class='mt-12 text-help']"
        )
        name_of_company = " ".join(elem_text_response.text.split(',')[:-1])

        logger.info(f'True_check_inn - {inn}')
        df = df.append(
            {
                'inn': inn,
                'name_of_company': name_of_company,
                'IT_accreditation': "True"
            },
            ignore_index=True
        )
        logger.info(f'Finish_check_inn - {inn}')
        return df

    except NoSuchElementException:
        logger.info(f'False_check_inn - {inn}')
        df = df.append(
            {
                'inn': inn,
                'name_of_company': np.NAN,
                'IT_accreditation': "False"
            },
            ignore_index=True
        )
        logger.info(f'Finish_check_inn - {inn}')
        return df


def connect_web():
    """
    Создаем элемент класса webdriver
    :return: driver: элемент класса webdriver
    """

    try:
        logger.info('Driver setup and site connection')

        path_driver = r'Drivers\chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=path_driver)

        logger.info('Connection succeeded')
        return driver

    except Exception as Error_connect_selenium:
        logger.exception(f'Error connecting to site. {Error_connect_selenium}')
        return False


def back_in_input_form(driver: object = webdriver, delay=10):
    """
    Функция для возврата к полю ввода
    :param driver: элемент класса браузера (browser class element);
    :param delay: время задержки для поиска (delay time for search)
    """

    elem_return_button = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='link-plain small']")))
    elem_return_button.click()


def work_selenium(logger: object = logging,
                  inn_list: object = list,
                  index_inn_list: int = 0,
                  df_verified_inn: object = pd.DataFrame()
                  ) -> pd.DataFrame:
    """
    Функция работы selenium (Selenium work function)
    @param logger: настройки логгирования (logging settings);
    @param inn_list: список с инн компаний (list with inn of companies);
    @param index_inn_list: индекс списка inn_list,
    с которого начнется новая проверка; (the index of the inn_list from which the new check will start);
    @param df_verified_inn: Data Frame для записи результатов (Data Frame for recording results);
    @return: Data Frame с результатами проверки (Data Frame with test results);
    """

    driver = connect_web()

    try:
        logger.info(f'Getting started with the site {index_inn_list}')
        driver.get('https://www.gosuslugi.ru/itorgs')
        delay = 6  # seconds
        while index_inn_list < len(inn_list):
            try:
                inn = inn_list[index_inn_list]

                # Вводим данные в форму ввода
                logger.info(f'Search_inn_{inn}')
                input_data(driver, delay, inn)

                # Записывает результат поиска
                df_verified_inn = check_response(driver, df_verified_inn, inn)

                # Возвращаемся к полю ввода
                logger.info(f'Back_in_search_string - {inn}')
                back_in_input_form(driver, delay)

                index_inn_list += 1
                if index_inn_list % 50 == 0:
                    driver.close()
                    time.sleep(60)
                    return work_selenium(logger, inn_list, index_inn_list, df_verified_inn)

            except Exception as Error_work_selen:
                logger.exception(f'Error search inn {inn}. {Error_work_selen}')

        logger.info(f'Finish work selenium')
        return df_verified_inn

    except Exception as Error_connect_site:
        logger.exception(f'Error connecting to site. {Error_connect_site}')
        return df_verified_inn


if __name__ == '__main__':
    logger = logging_work()
    inn_list = read_csv_inn_com(logger)
    df_verified_inn = work_selenium(logger, inn_list)
    df_verified_inn.to_csv(f'Result_work_selenium.csv', index=False, encoding='utf-8-sig')
