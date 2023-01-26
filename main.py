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


def logging_work():
    """
    Настройки для логгирования скрипта;
    Script logging settings;
    """

    py_logger = logging.getLogger(__name__)
    py_logger.setLevel(logging.INFO)

    py_handler = logging.FileHandler(f"log_for_work.log", mode='w')
    py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

    py_logger.info(f"Begin logging {__name__}")

    return py_logger


def read_csv_inn_com(logger):
    """
    Функция для получения инн компаний из csv-файла;
    Function to get company TIN from csv file;

    :return: inn_list - список инн компаний (list of inn companies);
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


def check_response(driver, df, inn):
    """
    Функция проверки и записи в df;
    The function of checking and writing to df;

    :input:
            driver - элемент класса браузера (browser class element);
            df - Data Frame для записи результатов (Data Frame for recording results);
            inn - инн компании (inn company)

    :return:
            df - Data Frame с новыми данными ( Data Frame with new data);
    """

    delay = 2
    logger.info(f'Start_check_inn - {inn}')
    try:
        check_element_response = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, "//img[@class='img-ok']"))
        )
        elem_text_response = driver.find_element(By.XPATH, "//div[@class='mt-12 text-help']")

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


def work_selenium(logger, inn_list, index_inn_list=0, df_verified_inn=pd.DataFrame()):
    """
    Функция работы selenium;
    Selenium work function;

    :input:
            logger - настройки логгирования (logging settings);
            inn_list - список с инн компаний (list with inn of companies);
            index_inn_list - индекс списка inn_list, с которого начнется новая проверка
            (the index of the inn_list from which the new check will start)
            df_verified_inn - Data Frame для записи результатов (Data Frame for recording results);

    :return:
            df_verified_inn - Data Frame с результатами проверки (Data Frame with test results);
    """

    try:
        logger.info(f'Driver setup and site connection')

        path_driver = r'Drivers\chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=path_driver)

        logger.info(f'Connection succeeded')

    except Exception as Error_connect_selenium:
        logger.exception(f'Error connecting to site. {Error_connect_selenium}')
        return False

    try:
        logger.info(f'Getting started with the site {index_inn_list}')
        driver.get('https://www.gosuslugi.ru/itorgs')
        delay = 6  # seconds
        while index_inn_list < len(inn_list):
            try:
                inn = inn_list[index_inn_list]
                logger.info(f'Search_inn_{inn}')
                elem_search_string = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@class='search-input ng-untouched ng-pristine ng-valid']")))
                elem_search_string.clear()
                elem_search_string.send_keys(inn)
                elem_search_string.click()
                elem_search_string.send_keys(Keys.ENTER)

                df_verified_inn = check_response(driver, df_verified_inn, inn)

                logger.info(f'Back_in_search_string - {inn}')
                elem_return_button = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='link-plain small']")))
                elem_return_button.click()

                index_inn_list += 1
                if index_inn_list % 50 == 0:
                    driver.close()
                    logger.info(f'new_crusade')
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
