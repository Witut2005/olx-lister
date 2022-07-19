import os

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-city', help='in which city you want to search offers', required=False, default='Warszawa')
parser.add_argument('-thing', help='what type of thing do you want to find', required=False, default='komputer')
parser.add_argument('-pages', help='how many pages do you want to print', required=False, default=0xFFFFFFFF)
parser.add_argument('-results', help='how many results do you want to print', required=False, default=0xFFFFFFFF)

args = parser.parse_args()
pages = int(args.pages)
results = int(args.results)

DRVR_PATH = str(os.environ["HOME"]) + "/chromedriver/chromedriver"

driver = webdriver.Chrome(DRVR_PATH)
driver.get("https://www.olx.pl/")

driver.implicitly_wait(10)

city = driver.find_element(By.ID, 'cityField')
thing = driver.find_element(By.ID, 'headerSearch')
search = driver.find_element(By.ID, 'submit-searchmain')

must_be_clicked = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')

must_be_clicked.click()
city.send_keys(str(args.city))
time.sleep(1)
thing.send_keys(str(args.thing))
time.sleep(1)
thing.send_keys(Keys.RETURN)
time.sleep(1)
search.submit()

results_counter = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/form/div[4]/div[2]/h3/div')

print(results_counter.text)

if str(results_counter.text) == 'Znaleźliśmy 0 ogłoszeń':
    driver.quit()
    sys.exit('no results')

base_site = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/li[1]/a')
last_site = str(base_site.get_property('href')) + "?page=25"

current_site = None

for x in range(0, pages):

    if current_site is not None:
        time.sleep(1)
        if current_site == last_site:
            driver.quit()
            sys.exit('end of results')

    try:
        next_site = driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/a[2]')

    except selenium.common.exceptions.NoSuchElementException:
        try:
            next_site = driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/section[1]/div/ul/a[1]')
        except:
            driver.quit()
            sys.exit('end of results')

    offers = driver.find_elements(By.XPATH,
                                  '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/div[2]/div/a/div/div/div/div/h6')
    prices = driver.find_elements(By.XPATH,
                                  '//*[@id="root"]/div[1]/div[2]/form/div[5]/div/div[2]/div/a/div/div/div/div/p[@class="css-wpfvmn-Text eu5v0x0"]')

    for offer, price in zip(offers, prices):
        if results == 0:
            sys.exit('end of results')

        print(f"{offer.text:<70} {price.text}")
        print('--------------------')
        results -= 1

    current_site = next_site.get_property('href')

    next_site.click()
