from deeppavlov import train_model
from deeppavlov.core.commands.train import train_evaluate_model_from_config
from deeppavlov.core.commands.utils import parse_config
import os

# 경로 설정
config_path = "/app/deep_pavlov_config.json"
downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.makedirs(downloads_path, exist_ok=True)

# Config 파싱
config = parse_config(config_path)

# 모델 학습
train_evaluate_model_from_config(config)
