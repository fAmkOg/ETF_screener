#!/usr/bin/env python3

from selenium import webdriver

# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
# ,StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
import time
# import re
# from pathlib import Path

import undetected_chromedriver as udchr


def getURL(b, URL, element):
    b.get('about:blank')
    while True:
        try:
            b.get(URL)
            break
        except (TimeoutException, WebDriverException):
            print('Timeout...')

    print(URL, flush=True)
    timer = 0
    while (not b.find_elements(By.XPATH, element) or not b.find_element(By.XPATH, element).is_enabled() or not b.find_element(By.XPATH, element).is_displayed()) and b.current_url == URL:
        time.sleep(5)
        timer = (timer+1) % 30
        if timer == 0:
            b.get('about:blank')
            try:
                b.get(URL)
            except WebDriverException:
                pass


#
def ETF_scan_US(b):
    # scan US ETF
    url = 'https://etfdb.com/screener/#page=1'
    getURL(
        b, url, '//*[@id="mobile_table_pills"]/div[1]/div/div[1]/table/tbody/tr[25]')

    with open('ETF_us.csv', 'w', encoding='utf-8') as f:
        print('SYMBOL|NAME|CLASS|ASSET|YTD_CHG|AVGVOL_3M|PE_PRICE',
              file=f, flush=True)
        page = 1
        while (page <= 50):
            print(page)
            try:
                b.get('about:blank')
                b.get('https://etfdb.com/screener/#page=' + str(page))
            except WebDriverException:
                continue
            time.sleep(1)
            if b.find_elements(By.XPATH, '//*[@id="turnstile-wrapper"]'):
                _ = input("ENTER after verify...")

            if not b.find_elements(By.CSS_SELECTOR, "#mobile_table_pills > div.bootstrap-table.screener-table-overview > div > div.fixed-table-pagination > div > ul > li.active.page-number"):
                continue
            curr_pg = b.find_element(
                By.CSS_SELECTOR, "#mobile_table_pills > div.bootstrap-table.screener-table-overview > div > div.fixed-table-pagination > div > ul > li.active.page-number").text
            # print(pi,row)
            if int(curr_pg) != int(page):
                continue

            for i in range(25):
                tr = b.find_element(
                    By.XPATH, '//*[@id="mobile_table_pills"]/div[1]/div/div[1]/table/tbody/tr[' + str(i+1) + ']')
                print(tr.find_element(By.XPATH, './/td[1]').text,
                      tr.find_element(By.XPATH, './/td[2]').text,
                      tr.find_element(By.XPATH, './/td[3]').text,
                      tr.find_element(By.XPATH, './/td[4]').text,
                      tr.find_element(By.XPATH, './/td[5]').text,
                      tr.find_element(By.XPATH, './/td[6]').text,
                      tr.find_element(By.XPATH, './/td[7]').text,
                      sep='|', file=f, flush=True)

            page = page+1

# end ETF_scan

# MAIN


def main():
    # ETFcn: https://fund.eastmoney.com/data/gmbddetail.html#dt8;t2021_1;pi1;pn50;stdesc;scqmjzc
    # ETFus: https://etfdb.com/screener/#tab=overview&page=1

    try:
        options = webdriver.ChromeOptions()
        # capabilities = DesiredCapabilities.CHROME.copy()
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.socks_proxy = "127.0.0.1:8964"
        proxy.socksVersion = 5
        # proxy.add_to_capabilities(capabilities)
        
        # options.proxy = proxy

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")


        # cr_srv = Service(Path('~/chromedriver').expanduser())

        # b = Chrome(service=cr_srv)
        # b = Chrome(service=cr_srv, options=options )
        b = udchr.Chrome()
        
        # b = Chrome(service=cr_srv, desired_capabilities=capabilities)
        # b = Chrome('~/chromedriver')
        b.maximize_window()

        ETF_scan_US(b)
    #
    except (KeyboardInterrupt, NoSuchWindowException):
        print('exit...')
    finally:
        print("quit browser")
        # b.quit()


if __name__ == '__main__':
    main()
