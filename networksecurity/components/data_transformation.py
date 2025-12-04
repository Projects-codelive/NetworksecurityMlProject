import sys, os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import ( DataTransformationArtifact, DataValidationArtifact )
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

""" Data Transformation Steps
1. Data Transformation Config (Define constant -> data Transformation Config)
2. Initiate Data Transformation
3. Read Data from data Validation Artifact (train and test)
4. Data Transformation Steps
a. From train dataset droping the target column
b. SMOTETomek for fixing imbalance dataset
"""

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # 1. Reading data train and test from data validation artifact
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # KNN Imputer
    def get_data_transformer_object(cls)->Pipeline:
        """ It initialises a KNNImputer object with the parameter specified in the training_pipeline.py file
        and return a pipeline object with the KNNImputer object as the first step
        Args:
            cls: DataTransformation
        Returns:
              A Pipeline object
        """
        logging.info("Entered get_data_transformer_object method of transformation class")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNN Imputer initialized")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Initiating Data Transformation")
        try:
            logging.info("Starting Data Transformation")
            # 1. Reading data train and test from data validation artifact
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # 2. Seperating train feature and test feature
            # Training Feature
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            # Testing Feature
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            # 3. KNN Imputer
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformd_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformd_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformd_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformd_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            # preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)