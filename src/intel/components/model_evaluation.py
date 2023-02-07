import os,sys
import joblib
import numpy as np
from src.intel.configuration.s3_opearations import S3Sync
from src.intel.logger import logging
from src.intel.exception import CustomException
from src.intel.constants import *
from src.intel.entity.config_entity import *
from src.intel.entity.artifact_entity import *
from src.intel.entity.custom_model import *
from src.intel.utils import *
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, 
    data_ingestion_artifacts=DataIngestionArtifacts,
    model_trainer_artifacts = ModelTrainerArtifacts) -> None:
        self.model_evaluation_config = model_evaluation_config
        self.data_ingestion_artifact = data_ingestion_artifacts
        self.model_trainer_artifacts = model_trainer_artifacts

    def get_test_data_loader(self,test_data):
        try:
            logging.info("Enter the load_dataset method of model evaluation")
            test_dl = DataLoader(test_data, BATCH_SIZE, shuffle=SHUFFLE, num_workers=NUM_WORKERS,pin_memory=PIN_MEMORY)
            return test_dl
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_best_model_path(self):
        try:
            model_path = self.model_evaluation_config.s3_model_path
            best_model_dir = self.model_evaluation_config.best_model_dir
            os.makedirs(os.path.dirname(best_model_dir), exist_ok=True)

            s3_sync = S3Sync()
            best_model_path = None
            s3_sync.sync_folder_from_s3(
                folder=best_model_dir, aws_bucket_url=model_path)
            for file in os.listdir(best_model_dir):
                if file.endswith(".pt"):
                    best_model_path = os.path.join(best_model_dir, file)
                    logging.info(f"Best model found in {best_model_path}")
                    break
                else:
                    logging.info("Model is not available in best_model_directory")

            return best_model_path

        except Exception as e:
            raise CustomException(e, sys)

    def get_model(self,test_data):
        try:
            logging.info("getting the pre-trained resnet model")

            num_classes = len(test_data.classes)

            model = ResNet9(3,num_classes)

            return model

        except Exception as e:
            raise CustomException(e, sys)


    def evaluate_model(self):
        try:
            transformer_object = joblib.load(self.model_trainer_artifacts.transformer_object_path)

            test_data = ImageFolder(self.data_ingestion_artifact.test_file_path,
            transform = transformer_object)

            test_dl = self.get_test_data_loader(test_data)
            best_model_path = self.get_best_model_path()
            if best_model_path is not None:
                # load back the model
                model = self.get_model(test_data=test_data)
                logging.info("load production model to GPU")
                DEVICE = get_default_device()
                model = to_device(model, DEVICE)
                model.load_state_dict(torch.load(self.model_evaluation_config.best_model))
                model.eval()
                logging.info(f"load the data to {DEVICE}")
                test_dl = DeviceDataLoader(test_dl, DEVICE)
                logging.info("evaluate production model on test data")
                result = evaluate(model=model, val_loader=test_dl)

                s3_model_loss = result["val_loss"]
            
            else:
                logging.info("Model is not found on production server, So couldn't evaluate")
                s3_model_loss = None

            return s3_model_loss

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self):
        try:
            logging.info("Initiating the model evaluation component...")

            s3_model_loss = self.evaluate_model()
            print("s3_model_loss",s3_model_loss)

            tmp_best_model_loss = np.inf if s3_model_loss is None else s3_model_loss
            trained_model_loss = self.model_trainer_artifacts.result["val_loss"]
            print(trained_model_loss, BASE_LOSS)
            print(trained_model_loss < BASE_LOSS)

            evaluation_response = tmp_best_model_loss > trained_model_loss and trained_model_loss < BASE_LOSS

            model_evaluation_artifacts = ModelEvaluationArtifacts(
                s3_model_loss=tmp_best_model_loss,
                is_model_accepted=evaluation_response,
                trained_model_path=os.path.dirname(
                self.model_trainer_artifacts.model_path),
                s3_model_path=self.model_evaluation_config.s3_model_path
            )
            logging.info(f"Model evaluation completed! Artifacts: {model_evaluation_artifacts}")
            logging.info("model training completed")
            return model_evaluation_artifacts
            
        except Exception as e:
            raise CustomException(e, sys)
