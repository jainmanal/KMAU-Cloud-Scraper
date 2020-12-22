import json
import re
import traceback

import requests
from bs4 import  BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options



headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
# print(html)

def Reviews_dt(url,driver):
    try:
        driver.get(url)




        rev = driver
        review = []
        while rev:

            review_id = rev.find_elements_by_class_name('yotpo-review')
            r_txt = rev.find_elements_by_class_name('content-review')
            for id,txts in zip(review_id,r_txt):
                id=id.get_attribute('data-review-id')
                text = txts.get_attribute('textContent')
                review.append({'submissionId': id
                          , 'text': text})

            # rating = rev.find_element_by_class_name('sr-only')
            # rating = re.search(r'[\d]+.[\d]+', rating.get_attribute('textContent'))
            # print(id, rating.group(0))

            cont = rev.find_element_by_class_name('yotpo-reviews')
            cont = cont.find_element_by_class_name('yotpo-pager')
            lnk = cont.find_element_by_css_selector('.yotpo .yotpo-pager .yotpo-page-element.yotpo-icon-right-arrow')
            url = lnk.get_attribute('href')
            url1 = re.search(r'[https://www.kmart.com.au/product]*', url).group(0)
            print("url printing",url1)
            if url1:
                # print(url)
                rev.get(str(url))
            else:
                raise Exception('No Url for the next page')


    except Exception as e:
        # print(review)
        if 'no such element' in str(e) :
            # traceback.print_tb(e.__traceback__)
            pass
        elif 'No Url for the next page' in str(e):
            pass

    finally:
        check = bool(review)
        # print(check)
        if check:
            # print(review)
            return review
        else:
            return "NULL"
# Reviews_dt('https://www.kmart.com.au/product/the-last-kids-on-earth-and-the-midnight-blade-by-max-brallier---book/3291323','l')
