# Импорт библиотек
# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from zipfile import ZipFile


def connect():

    driver = webdriver.ChromiumEdge()
    driver.get("https://www.gosuslugi.ru/itorgs")
    pass


if __name__ == '__main__':
    connect()
