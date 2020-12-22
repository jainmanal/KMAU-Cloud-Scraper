import re

from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from db import dataBase, connection



driver = Chrome()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
db = connection()

try:
    link = requests.get('https://www.kmart.com.au/sitemap-core.xml',headers=headers)
    link = BeautifulSoup(link.text,'html.parser')
    link = link.findAll('loc')
    cont = 0
    for lnk in link:
        if re.search(r'^[https://www.kmart.com.au/product].*[\d]$',lnk.text):
            if cont<1640:
                cont+=1
                continue
            dataBase(lnk.text,db,driver)

except Exception as e:
    print(e)

driver.close()