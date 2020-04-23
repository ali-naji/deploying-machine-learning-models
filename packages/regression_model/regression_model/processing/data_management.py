import pandas as pd
import joblib
from sklearn.pipeline import Pipeline

from regression_model.config import config
from regression_model import __version__ as _version
import boto3
import os
import logging


_logger = logging.getLogger(__name__)
s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))


def load_dataset(*, file_name: str) -> pd.DataFrame:
    save_dir = (config.DATASET_DIR / file_name).absolute().as_posix()

    s3.download_file("house-price-regression-data", file_name, save_dir)
    _data = pd.read_csv(f"{config.DATASET_DIR}/{file_name}")
    return _data


def save_pipeline(*, pipeline_to_persist) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
    save_path = config.TRAINED_MODEL_DIR / save_file_name
    os.environ['pipeline_save_path'] = save_path.absolute().as_posix()
    joblib.dump(pipeline_to_persist, save_path)
    _logger.info(f"saved pipeline: {save_file_name}")
    _logger.info(f"saved location: {save_path}")


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    trained_model = joblib.load(filename=os.environ.get('save_path'))
    return trained_model
