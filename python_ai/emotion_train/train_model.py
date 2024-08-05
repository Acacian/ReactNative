import os
import json
import logging
from deeppavlov import train_model
from deeppavlov.core.commands.utils import parse_config
from transformers import pipeline

logging.basicConfig(level=logging.INFO, filename='/app/train_model.log', filemode='w')

downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

logging.info(f"DOWNLOADS_PATH: {downloads_path}")

# DeepPavlov 설정 파일 로드 및 수정
with open("/app/deep_pavlov_config.json", "r") as config_file:
    config = json.load(config_file)

config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

# 감정 분류기 로드
emotion_classifier = pipeline('text-classification', model='/app/emotion_classifier')

def preprocess_with_emotion(text):
    # 텍스트에 대한 감정 분석 수행
    emotion = emotion_classifier(text)[0]['label']
    # 원본 텍스트에 감정 정보 추가
    return f"[EMOTION={emotion}] {text}"

# 데이터 전처리 함수 수정
config['dataset_reader']['preprocessor'] = preprocess_with_emotion

# 모델 훈련
logging.info("Starting model training...")
try:
    train_model(config)
    logging.info("Model training completed successfully.")
except Exception as e:
    logging.exception(f"Error during model training: {e}")

# 훈련된 모델을 사용한 간단한 테스트
from deeppavlov import build_model

model = build_model(config)

test_questions = [
    "오늘 기분이 너무 좋아!",
    "최근에 힘든 일이 많았어",
    "새로운 프로젝트를 시작하게 되어 설레",
    "친구와 크게 다퉜어"
]

for question in test_questions:
    emotion = emotion_classifier(question)[0]['label']
    response = model([question])
    logging.info(f"Q: {question}")
    logging.info(f"Detected Emotion: {emotion}")
    logging.info(f"A: {response[0]}")
    logging.info("---")

logging.info("Test completed")