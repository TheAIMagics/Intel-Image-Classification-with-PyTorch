from dataclasses import dataclass

# Data ingestion artifacts
@dataclass
class DataIngestionArtifacts:
    train_file_path: str
    test_file_path: str
    pred_file_path: str
    data_path :str


@dataclass
class DataValidationArtifact:
    validation_status: bool


@dataclass
class ModelTrainerArtifacts:
    model_path: str
    result: dict
    transformer_object_path: str