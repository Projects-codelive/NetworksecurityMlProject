import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        datainegestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(datainegestionconfig)
        logging.info("Data Ingestion Artifact Created")
        datainegestionartifact =  data_ingestion.initiate_data_ingestion()
        print(datainegestionartifact)
    except NetworkSecurityException as e:
        raise NetworkSecurityException(e,sys)