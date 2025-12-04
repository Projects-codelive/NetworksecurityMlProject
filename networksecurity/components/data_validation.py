# Data Valiadtion includes
# 1. Schema reamains the same i.e No. of columns(features) remain the same
# 2. Data Drift change in data
# 3. Validate No. of column and check if there is any numerical columns

"""Steps:
1. Initiate Data Validation
2. """

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # 2. Read the data from train and test csv
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # 3. Validate No. of columns
    def validate_number_of_columns(self, dataframe: pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data Frame has columns: {dataframe.columns}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # 4. Check if numerical column exist or not
    def is_numerical_column_exist(self, dataframe: pd.DataFrame)->bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=[np.number]).columns.tolist()
            if len(numerical_columns) > 0:
                logging.info(f"Numerical columns found: {numerical_columns}")
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # 5. Detect Data Drift in the dataframe
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status = True
            report={}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist=ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False   # There is a change in the distribution
                report.update({col: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found,
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            # Create a directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            # 1. To get the train and test file from data ingestion artifact
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # 2. Read the data from train and test csv
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            # 3. Validate No. of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contains all columns \n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contains all columns \n"
            # 4. Check if numerical column exist or not
            isNumerical = self.is_numerical_column_exist(train_dataframe)
            if isNumerical:
                error_message = f"Numerical columns found in Train dataframe  \n"
            isNumerical = self.is_numerical_column_exist(test_dataframe)
            if isNumerical:
                error_message = f"Numerical columns found in Test dataframe  \n"
            # 5. Detect Data Drift in the dataframe
            status = self.detect_dataset_drift(train_dataframe, test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            data_validaation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validaation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)