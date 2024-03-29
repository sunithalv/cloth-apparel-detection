import os
import sys
from clothing.entity.config_entity import DataIngestionConfig
from clothing.entity.artifacts_entity import DataIngestionArtifacts
from clothing.configuration.s3_syncer import S3Sync
from clothing.exception import CustomException
from clothing.logger import logging
from clothing.constants import *
from zipfile import ZipFile


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        
        self.s3 = S3Sync()

    def get_data_from_s3(self) -> None:
        try:
            logging.info("Entered the get_data_from_s3 method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.s3.sync_folder_from_s3(folder=self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,bucket_name=self.data_ingestion_config.BUCKET_NAME,bucket_folder_name=self.data_ingestion_config.S3_DATA_DIR)


            logging.info("Exited the get_data_from_s3 method of Data ingestion class")
        except Exception as e:
            raise CustomException(e, sys) from e

    def unzip_and_clean(self):
        logging.info("Entered the unzip_and_clean method of Data ingestion class")
        try:
            zip_file_name = os.path.join(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,self.data_ingestion_config.ZIP_FILE_NAME)

            zip_obj = ZipFile(zip_file_name)

            zip_obj.extractall(path=self.data_ingestion_config.ZIP_FILE_DIR)

            logging.info("Exited the unzip_and_clean method of Data ingestion class")
            return self.data_ingestion_config.TRAIN_DATA_ARTIFACT_DIR, self.data_ingestion_config.TEST_DATA_ARTIFACT_DIR, self.data_ingestion_config.VALID_DATA_ARTIFACT_DIR
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of Data ingestion class")
        try:

            self.get_data_from_s3()

            logging.info("Fetched the data from S3 bucket")
            train_file_path, test_file_path, valid_file_path = self.unzip_and_clean()

            logging.info("Unzipped file and splited into train, test and valid")

            data_ingestion_artifact = DataIngestionArtifacts(train_file_path=train_file_path,
                                                             test_file_path=test_file_path,
                                                             valid_file_path=valid_file_path)

            logging.info("Exited the initiate_data_ingestion method of Data ingestion class")

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys) from e