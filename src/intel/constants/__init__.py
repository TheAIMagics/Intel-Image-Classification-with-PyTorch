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


# Model Training related constants
MODEL_TRAINER_ARTIFACT_DIR: str = "model_trainer"
MODEL_NAME: str = "model.pt"
BATCH_SIZE: int = 128
EPOCHS: int = 15
LEARNING_RATE:float = 0.001
GRAD_CLIP : float = 0.1
WEIGHT_DECAY : float = 1e-4
IN_CHANNELS: int = 3
OPTIMIZER = torch.optim.RMSprop
NUM_CLASSES :int = 6
TRANSFORM_OBJECT_NAME: str = "transform.pkl"

# constants realted to model evaluation 
S3_BUCKET_MODEL_URI: str = "s3://intel-image-data/model/"
MODEL_EVALUATION_DIR: str = "model_evaluation_artifacts"
S3_MODEL_DIR_NAME: str = "s3_model"
S3_MODEL_NAME: str = "model.pt"
BASE_LOSS: int = 4.00
SHUFFLE = True
PIN_MEMORY = True
NUM_WORKERS = 0

