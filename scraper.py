import ast
import datetime
import re
import time
import traceback

from bs4 import BeautifulSoup
import  requests
import json

from Review_data import Reviews_dt

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}

def scrap(url,driver):
        # driver = Chrome()
        print("scraping",url)
        try:
                details = {}
                driver.get(url)
                time.sleep(2)
                try:
                        req = driver.page_source
                        soup = BeautifulSoup(req, 'html.parser')
                        # print(soup)
                        data = soup.find('script', attrs={'type': 'application/ld+json'}).text
                        data = ast.literal_eval(data)
                except Exception as e:
                        print(e)
                        pass

                title = driver.find_element_by_class_name('title')
                details['name'] = title.text

                code = url.split('/')[-1]
                # print(type(code))

                details['_id'] = f"kmau_{code}"
                details['code'] = [code]
                details['prodCode'] = [code]
                details['varCode'] = [code]

                try:
                        price = driver.find_element_by_class_name('price')
                        price = re.search(r'[\d]*\.[\d]*',price.text).group(0)
                        # orgprice = driver.find_element_by_class_name('price')
                        # orgprice = orgprice.find_elements_by_tag_name('h4')
                        # for i in orgprice:
                        #         print(i)
                        # orgprice = re.search(r'[a-z]*[\d]+\.[\d]*',orgprice.text)
                        # print(orgprice)
                        details['price'] = price
                        details['orgprice']=""
                except:
                        details['price'] = "Null"
                        details['orgprice'] = ""
                try:
                        rating = driver.find_elements_by_class_name('yotpo-stars')
                        for ratin in rating:
                                ratin = re.search(r'[\d]+.[\d]+', ratin.get_attribute('textContent')).group(0)
                                print(ratin)
                        details['rating'] = ratin
                except:
                        details['rating'] = "Null"
                details['stock'] = 'null'
                details['URL'] = url
                details['deliveryMtd'] =""
                details['shipFrom'] = "AU"
                details['shipTo'] = ["TW", "HK", "JP", "UAE", "AU", "PH", "IN", "MY", "CN", "UK", "ID"]
                try:
                        if data:
                                details['imgsURL'] = data['image']
                        else:
                                img = driver.find_element_by_class_name('image')

                                img = img.find_elements_by_tag_name('img')
                                img_link = []
                                for i in img:
                                        img_link.append(i.get_attribute('src'))
                                details['imgsURL'] = img_link
                except:
                        details['imgsURL'] = "Not available"

                # Variant = url.split('/')
                # Variant = Variant[-3].split('-')
                # Variants = "".join(Variant[-2:])
                # details['variants'] = Variants
                details['variants'] =""

                # breadcrumb =[]
                try:
                        breadcrumb = driver.find_element_by_class_name('breadcrumbs')
                        breadcrumb = breadcrumb.text.split('\n')
                        # print(breadcrumb)
                        details['breadcrumb'] = breadcrumb
                except:
                        details['breadcrumb'] = "Not available"

                review = Reviews_dt(url, driver)
                details['reviews'] = review



                details['prodDescription'] = {}
                details['prodDescription']['shortDes']=""
                try:
                        if data:
                                details['prodDescription']['imgsURL'] = data['image']
                        else:
                                img = driver.find_element_by_class_name('image')
                                # img = driver.find_element_by_class_name('owl-stage-outer')
                                img = img.find_elements_by_tag_name('img')
                                img_link = []
                                for i in img:
                                        img_link.append(i.get_attribute('src'))
                                details['imgsURL'] = img_link
                except:
                        details['imgsURL'] = "Not available"

                try:
                        prodDetail = driver.find_element_by_class_name('tab-panel') #product-details-desc
                        prodDetail = prodDetail.get_attribute('innerHTML')
                        details['prodDescription']['detailDes'] = prodDetail
                except:
                        details['prodDescription']['detailDes']= "Not available"



                details['seller'] = {}
                try:
                        details['seller']['name'] = data['offers']['seller']['name']
                except:
                        details['seller']['name'] = ""
                details['seller']['URL'] = ""
                details['seller']['code'] = ""

                try:
                        details['rootProductcode'] = [code]
                        details["rootprice"] = price
                except:
                        details['rootProductcode'] = "Not Available"
                        details["rootprice"] = "Not Available"
                try:
                        details['Currency'] = data['offers']['priceCurrency']
                except:
                        details['Currency'] = "$"
                details['LastUpdateTime'] = datetime.datetime.utcnow()


        except Exception as e :
                traceback.print_tb(e.__traceback__)
                print(e)
        finally:
                if details:
                        return details
                else:
                        return None
# scrap('https://www.kmart.com.au/product/incredible-but-true:-dinosaurs---book/2580336')
