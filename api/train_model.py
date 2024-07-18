import os
import json
import logging
from deeppavlov import train_model
from deeppavlov.core.commands.utils import parse_config

logging.basicConfig(level=logging.INFO, filename='/app/train_model.log', filemode='w')

# DOWNLOADS_PATH 환경 변수 확인 및 설정
downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

logging.info(f"DOWNLOADS_PATH: {downloads_path}")

# config 파일 읽기 및 수정
with open("/app/deep_pavlov_config.json", "r") as config_file:
    config = json.load(config_file)

# DOWNLOADS_PATH를 직접 대체
config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

# 모델 훈련
logging.info("Starting model training...")
try:
    train_model(config)
    logging.info("Model training completed successfully.")
except Exception as e:
    logging.exception(f"Error during model training: {e}")