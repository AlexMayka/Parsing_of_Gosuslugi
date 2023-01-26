# Selenium_python
<h3>Обучение на selenium</h3> 

Скрипт для автоматизации получения данных из сайта "Госуслуги"

Цель:

Получить информицию о статусе акредитации it-компаний из сайта "Госуслуги" (https://www.gosuslugi.ru/itorgs) 

Входящие данные: <br>
Файл '.csv' с ИНН организаций (..\inn_org\inn_org.csv)

![input.png](img%input.png)

Технологии:<br>
<ul>
    <li>Язык программирования: Python 3.11.0</li>
    <li>Библиотеки:
        <ul>
            <li>Pandas</li>
            <li>Selenium</li>
            <li>Numpy</li>
            <li>Logging</li>
        </ul>
    </li>
</ul>

![example_performance.gif](img%2Fexample_performance.gif)

Процесс работы:

<ol>
    <li>Извлечение инн из ".csv" файла;</li>
    <li>Каждый из номеров проверить на сайте (selenium);</li>
    <li>Результат проверки номера записать в Data Frame (pandas);</li>
    <li>Записать результат в ".csv" файл.</li>
</ol>

Выходные данные:

Файл log_for_work.log. Лог-файл работы скрипта (отслеживание статуса выполнения)

![log.png](img%2Flog.png)

Файл с результатом работы Result_work_selenium.csv состоящий из:
<ul>
    <li>Колонка 1: inn - Идентификационный номер налогоплательщика компании</li>
    <li>Колонка 2: name_of_company - Наименование компании</li>
    <li>Колонка 3: IT_accreditation - Статус аккредитации-</li>
</ul>

![out.png](img%out.png)
