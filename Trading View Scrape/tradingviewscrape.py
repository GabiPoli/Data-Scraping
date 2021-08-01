import os
import time
from selenium import webdriver
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException,TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd


browser = webdriver.Chrome(r'C:\Users\User/chromedriver')
time.sleep(7)
browser.maximize_window()

urls = ['https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/']  

   
for url in urls: 
                
    browser.get(url)
   
    
    file_base_name = url.split('/')[-2]

    print(f'Scraping{url}...')

    
    xlwriter = pd.ExcelWriter(file_base_name + '.xlsx')


    categories = ['Overview','Performance','Valuation','Dividends','Margins','Income Statement','Balance Sheet','Oscillators','Trend-Following']


    for category in categories:
        print(f'Processing report: {category}')

        try:

            element_tab = browser.find_element_by_xpath(f'//div[text()="{category}"]')
            try:
                element_tab.click()
            except ElementNotInteractableException:
                pass   

            # delay for a table to load
            time.sleep(6)

            df = pd.read_html(browser.page_source)[0]
            df.replace('-','',inplace=True) #Replace - from clumun EV/EBITDA
            df.to_excel(xlwriter,sheet_name = category,index = False)

            
        except(NoSuchElementException, TimeoutException):
            print(f'Report {category} is not found')
            continue
               

    xlwriter.save()

browser.quit()
   
