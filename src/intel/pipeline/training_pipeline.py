import os,sys
from src.intel.components.data_ingestion import DataIngestion
from src.intel.components.data_validation import DataValidation
from src.intel.components.model_training import ModelTraining
from src.intel.components.model_evaluation import ModelEvaluation
from src.intel.components.mode_pusher import ModelPusher
from src.intel.logger import logging
from src.intel.exception import CustomException
from src.intel.entity.config_entity import *
from src.intel.entity.artifact_entity import *
from src.intel.configuration.s3_opearations import S3Operation

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()

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

    def start_model_trainer(self,data_ingestion_artifact : DataIngestionArtifacts):
        try:
            logging.info("Entered the start_model_trainer method of TrainPipeline class")
            
            model_trainer = ModelTraining(data_ingestion_artifact=data_ingestion_artifact,
            model_trainer_config=self.model_trainer_config)
            model_trainer_artifact =  model_trainer.initiate_model_trainer()
            logging.info("Exited the start_transformation method of TrainPipeline class")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def start_model_evaluation(self,data_ingestion_artifacts: DataIngestionArtifacts,model_trainer_artifacts: ModelTrainerArtifacts) -> ModelEvaluationArtifacts:
        logging.info("Starting model evaluation in training pipeline")
        try: 
            model_evaluation = ModelEvaluation(self.model_evaluation_config, data_ingestion_artifacts, model_trainer_artifacts)
            logging.info("Evaluating current trained model")
            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            logging.info("Model evaluation step completed successfully in train pipeline")
            return model_evaluation_artifacts
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_pusher(self, model_evaluation_artifacts: ModelEvaluationArtifacts):
        logging.info("Starting model pusher in training pipeline")
        try: 
            model_pusher = ModelPusher(model_evaluation_artifacts=model_evaluation_artifacts)
            logging.info("If model is accepted in model evaluation. Pushing the model into production storage")
            model_pusher_artifacts = model_pusher.initiate_model_pusher()
            logging.info("Model pusher step completed successfully in train pipeline")
            return model_pusher_artifacts
        except Exception as e:
            raise CustomException(e, sys)

    
    def run_pipeline(self) -> None:
        try:
            logging.info("=================Training pipeline Started =====================")
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            if data_validation_artifact.validation_status:
                model_trainer_artifact = self.start_model_trainer(data_ingestion_artifact=data_ingestion_artifact)
                model_evaluation_artifacts = self.start_model_evaluation(data_ingestion_artifact, model_trainer_artifact)
                if model_evaluation_artifacts.is_model_accepted:
                    model_pusher_artifact = self.start_model_pusher(model_evaluation_artifacts=model_evaluation_artifacts)

            logging.info("=================Training pipeline completed =====================")
                    
            
        except Exception as e:
            raise CustomException(e,sys) from e