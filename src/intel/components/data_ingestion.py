import os,sys
from zipfile import ZipFile, Path
from src.intel.logger import logging
from src.intel.exception import CustomException
from src.intel.constants import *
from src.intel.entity.config_entity import *
from src.intel.entity.artifact_entity import *
from src.intel.configuration.s3_opearations import S3Operation

class DataIngestion:
    def __init__(self, data_ingestion_config :DataIngestionConfig, S3_operations: S3Operation):
        self.data_ingestion_config = data_ingestion_config
        self.S3_operations = S3_operations

    def get_images_from_s3(self, bucket_file_name: str, bucket_name: str, output_filepath: str) -> zip:
        """
        Method Name :   get_images_from_s3
        Description :   This method will fetch compressed folder from s3 bucket and save it.
        """
        logging.info("Entered the get_data_from_s3 method of Data ingestion class")
        try:
            if not os.path.exists(output_filepath):
                self.S3_operations.read_data_from_s3(bucket_file_name,bucket_name,output_filepath)

            logging.info("Exited the get_data_from_s3 method of Data ingestion class")

        except Exception as e:
            raise CustomException(e, sys) from e

    def unzip_data(self, zip_data_filepath: str) -> Path:
        """
        Method Name :   unzip_file
        Description :   This method will unzip folder and save it.
        """
        logging.info("Unzipping the downloaded zip file from download directory...")
        try:
            if os.path.isdir(zip_data_filepath):
                logging.info(f'Unzipped folder already exist in {zip_data_filepath}')
            else:
                with ZipFile(zip_data_filepath, mode='r') as zip_ref:
                    zip_ref.extractall(self.data_ingestion_config.data_ingestion_artifact_dir)

                logging.info(f"Unzipping of data completd and extracted at {self.data_ingestion_config}")
        except Exception as e:
            raise CustomException(e, sys) from e
    

    def initiate_data_ingestion(self) ->DataIngestionArtifacts:
        try:
            logging.info("Initiating the data ingestion component...")

            os.makedirs(self.data_ingestion_config.data_ingestion_artifact_dir, exist_ok=True)
            logging.info(
                f"Created {os.path.basename(self.data_ingestion_config.data_ingestion_artifact_dir)} directory."
            )
            self.get_images_from_s3(bucket_file_name=S3_DATA_FOLDER_NAME, bucket_name=BUCKET_NAME,output_filepath=self.data_ingestion_config.zip_data_path) 

            # Unzipping the file
            self.unzip_data(zip_data_filepath=self.data_ingestion_config.zip_data_path)

            data_ingestion_artifact = DataIngestionArtifacts(
                train_file_path= self.data_ingestion_config.train_path,
                test_file_path=self.data_ingestion_config.test_path,
                pred_file_path=self.data_ingestion_config.pred_path,
                data_path= self.data_ingestion_config.data_path
            )
            logging.info(f"Data Ingestion Artifact {data_ingestion_artifact}")

            logging.info('Data ingestion is completed Successfully.')

            return data_ingestion_artifact
            
        except Exception as e:
            raise CustomException(e, sys) from e