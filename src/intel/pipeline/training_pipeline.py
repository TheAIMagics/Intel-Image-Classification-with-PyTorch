import os,sys
from src.intel.components.data_ingestion import DataIngestion
from src.intel.components.data_validation import DataValidation
from src.intel.logger import logging
from src.intel.exception import CustomException
from src.intel.entity.config_entity import *
from src.intel.entity.artifact_entity import *
from src.intel.configuration.s3_opearations import S3Operation

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self)-> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the compressed data from S3 Bucket")
            data_injestion_obj  = DataIngestion(data_ingestion_config = self.data_ingestion_config, S3_operations=S3Operation())
            data_ingestion_artifact = data_injestion_obj.initiate_data_ingestion()
            logging.info("Got the extracted data ")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact : DataIngestionArtifacts)-> DataValidationArtifact:
        try:
            logging.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def run_pipeline(self) -> None:
        try:
            logging.info("=================Training pipeline Started =====================")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            print(data_validation_artifact)
            
        except Exception as e:
            raise CustomException(e,sys) from e