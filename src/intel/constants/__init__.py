import os
import torch
from from_root import from_root


ARTIFACTS_DIR: str = "artifacts"
SOURCE_DIR_NAME: str = "src"

ZIP_FILE_NAME: str = "data.zip"
TRAIN_FOLDER_NAME : str = 'seg_train'
TEST_FOLDER_NAME : str = 'seg_test'
PRED_FOLDER_NAME : str = 'seg_pred'


# Data Ingestion related constants
ARTIFACTS_DIR = os.path.join(from_root(), "artifacts")
BUCKET_NAME = 'intel-image-data'
S3_DATA_FOLDER_NAME = "data.zip"
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestion"
UNZIP_FOLDER_NAME = 'data/'

# Data Validation related constants
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")



