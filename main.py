from selenium import webdriver
from selenium.webdriver.common.by import By
from pandas import DataFrame

URL = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'
PAGES = 32

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--headless=new")
OPTIONS.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=OPTIONS)

table_data = []


def add_data():
    thead = driver.find_element(By.XPATH, value='//*[@id="__next"]/div/div[1]/article/div[2]/table/thead')
    header_names = thead.find_elements(By.CSS_SELECTOR, value='tr th')

    column_header = [header.text for header in header_names]

    table_rows = driver.find_elements(By.CSS_SELECTOR, value='tr.data-table__row')

    for row in table_rows:
        row_values = row.find_elements(By.CSS_SELECTOR, value='span.data-table__value')
        row_data = {}
        for index, value in enumerate(row_values):
            data = value.text
            if '$' in data:
                salary = data.split('$')[1]
                data = int(salary.replace(',', ''))
            row_data[column_header[index]] = data
        table_data.append(row_data)


if __name__ == '__main__':
    for page_num in range(0, PAGES):
        page = page_num + 1
        driver.get(f'{URL}/page/{page}')
        add_data()
        print(f'added data from page {page}')

    table_dataDF = DataFrame(table_data)
    table_dataDF.to_csv('salary.csv')

    driver.quit()
