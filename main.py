import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
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
        logging.info("Data Ingestion Completed")
        print(datainegestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(datainegestionartifact, data_validation_config)
        logging.info("Initiate Data Validation Artifact")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)


    except NetworkSecurityException as e:
        raise NetworkSecurityException(e,sys)


# Data Valiadtion includes
# 1. Schema reamains the same i.e No. of columns(features) remain the same
# 2. Data Drift change in data
# 3. Validate No. of column
