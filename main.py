import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, \
    ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        datainegestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(datainegestionconfig)
        logging.info("Data Ingestion Artifact Created")
        datainegestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(datainegestionartifact)

        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(datainegestionartifact, data_validation_config)
        logging.info("Initiate Data Validation Artifact")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

        logging.info("Data Validation Artifact initiated")
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

        logging.info("Initiate Model Training Artifact")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer =ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training Completed")
    except NetworkSecurityException as e:
        raise NetworkSecurityException(e, sys)