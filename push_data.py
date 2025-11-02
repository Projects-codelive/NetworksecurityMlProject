# ETL(Extract Transform Load) Pipeline
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()
# certifi is a python package that provides the root certificates it is commonly used by python library that needs
# to make a secure http connection here we are making http connection with mongodb
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

# Reading the data and converting to json file
    def cv_to_json_convertor(self, file_path):
        try:
            data=pd.read_csv(file_path)
            # by default csv has already index
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())  ## T means transpose and  converts a pandas DataFrame into a list of dictionaries
            # print(records)
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)  # It is use for connecting to mongodb
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="Networking"
    Collection="NetworkData"
    networkobj = NetworkDataExtract()
    records=networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)