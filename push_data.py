# ETL(Extract Transform Load) Pipeline
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()
# certifi is a python package that provides the root certificates it is commonly used by python library that needs
# to make a secure http connection here we are making http connection with mongodb
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

# reading the dataset and converting it into json format
    def cv_to_json_convertor(self, file_path):
        try:
            df = pd.read_csv(file_path)
            # reseting the index
            df.reset_index(drop=True, inplace=True)
            # df.to_json() returns a JSON string, not a Python list or dictonary so it cannot be used
            # record = df.to_json(orient='records')

            # The to_json() method returns a JSON - formatted string
            record = json.loads(df.to_json(orient='records'))
            # print(record)
            return record
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, record, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.record = record
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            # PyMongo's insert_many() requires a list of dictionaries
            self.collection.insert_many(self.record)
            return (len(self.record))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    file_path = "Network_Data/phisingData.csv"
    DATABASE = "Networking"
    COLLECTION = "Network_Data"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json_convertor(file_path)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)
