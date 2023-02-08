import os
import sys
import torch
import joblib
from PIL import Image
from src.intel.exception import CustomException
from src.intel.entity.custom_model import *
from src.intel.entity.config_entity import *
from src.intel.entity.artifact_entity import *
from src.intel.configuration.s3_opearations import S3Sync
from src.intel.utils import *

DEVICE = get_default_device()

class SinglePrediction:
    def __init__(self):
        try: 
            self.s3_sync = S3Sync()
            self.prediction_config = PredictionPipelineConfig()
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_model_in_production(self):
        try:
            s3_model_path = self.prediction_config.s3_model_path
            model_download_path = self.prediction_config.prediction_artifact_dir
            os.makedirs(model_download_path, exist_ok=True)
            if len(os.listdir(model_download_path)) == 0:
                self.s3_sync.sync_folder_from_s3(folder=model_download_path, aws_bucket_url=s3_model_path)
        except Exception as e:
            raise CustomException(e, sys)

    def get_model(self):
        try:
            self.get_model_in_production()

            prediction_model_path = self.prediction_config.model_download_path

            prediction_model = to_device(ResNet9(3,NUM_CLASSES), DEVICE)

            prediction_model.load_state_dict(torch.load(prediction_model_path, map_location=torch.device('cpu')))

            # for gpu devices
            # prediction_model.load_state_dict(torch.load(prediction_model_path))

            prediction_model.eval()

            return prediction_model
            
        except Exception as e:
            raise CustomException(e, sys)

    def _get_image_tensor(self, image_path):
        try:
            img = Image.open(image_path)
            transforms = joblib.load(self.prediction_config.transforms_path)
            img_tensor = transforms(img)

            return img_tensor
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, image_path):
        try:
            self.get_model_in_production()
            
            model = self.get_model()

            image = self._get_image_tensor(image_path)

            result = predict_image(image, model, DEVICE, NUM_CLASSES)

            return result
        except Exception as e:
            raise CustomException(e, sys)