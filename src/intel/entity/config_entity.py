import os
import sys
from zipfile import Path, ZipFile
from dataclasses import dataclass
from src.intel.constants import *
from datetime import datetime
from from_root import from_root


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class DataIngestionConfig:
    data_ingestion_artifact_dir: str = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
    zip_data_path : str = os.path.join(data_ingestion_artifact_dir, S3_DATA_FOLDER_NAME)
    data_path: str = os.path.join(data_ingestion_artifact_dir, UNZIP_FOLDER_NAME)
    train_path : str = os.path.join(data_path,TRAIN_FOLDER_NAME)
    test_path : str = os.path.join(data_path,TEST_FOLDER_NAME)
    pred_path : str = os.path.join(data_path,PRED_FOLDER_NAME)


@dataclass
class DataValidationConfig:
    schema_file_path = os.path.join("config", "schema.yaml")

@dataclass
class ModelTrainerConfig:
    model_trainer_artifact_dir = os.path.join(from_root(), ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACT_DIR)
    model_path: str = os.path.join(model_trainer_artifact_dir, MODEL_NAME)
    transformer_object_path: str = os.path.join(model_trainer_artifact_dir, TRANSFORM_OBJECT_NAME)

@dataclass
class ModelEvaluationConfig:
    s3_model_path: str = S3_BUCKET_MODEL_URI
    model_evaluation_artifacts_dir: str = os.path.join(from_root(), ARTIFACTS_DIR, MODEL_EVALUATION_DIR)
    best_model_dir: str = os.path.join(model_evaluation_artifacts_dir, S3_MODEL_DIR_NAME)
    best_model: str = os.path.join(best_model_dir, S3_MODEL_NAME)

@dataclass
class PredictionPipelineConfig:
    s3_model_path: str = S3_BUCKET_MODEL_URI
    prediction_artifact_dir = os.path.join(from_root(),  ARTIFACTS_DIR,PREDICTION_PIPELINE_DIR_NAME)
    model_download_path = os.path.join(prediction_artifact_dir, MODEL_NAME)
    transforms_path = os.path.join(prediction_artifact_dir, TRANSFORM_OBJECT_NAME)