import json
import datetime

import pymongo
import dns # required for connecting with SRV
from bson import json_util
import traceback
from scraper import scrap




def connection():
     try:
          client = pymongo.MongoClient("mongodb+srv://superchain:superchain@cluster0.clwzb.mongodb.net/test")
          # print(client.list_database_names())
     except Exception as e:
          traceback.print_tb(e.__traceback__)
          print(e)
     db = client['products']
     db = db['km_au']
     return db




def dataBase(url,db,driver):

          data = scrap(url,driver)
          try:
               check = not bool(data)
               if check:
                    print(check)
                    raise Exception("Null Data")
               try:
                    db.insert_one(data)
                    print("inserting")
                    print("inserted")
                    # return "inserted"
               except pymongo.errors.DuplicateKeyError as e:
                    print("Updating records, details are already exist", e)
                    db.update({"_id": data['_id']},
                              {"$set": {"price": data['price'], "stock": data['stock']
                                   ,"rating": data["rating"],"rootprice": data['rootprice'],'reviews':data['reviews'],'LastUpdateTime':data['LastUpdateTime']}})
                    print("Updated")

          except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print('Error is ', e)
                    print("not inserted")

# dataBase("https://www.kmart.com.au/category/toys/toys-by-category/action-figures/beyblades/465504",connection(),driver)

