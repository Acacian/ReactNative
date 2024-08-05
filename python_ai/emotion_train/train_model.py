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
    emotion = emotion_classifier(text)[0]['label']
    return f"[EMOTION={emotion}] {text}"

config['dataset_reader']['preprocessor'] = preprocess_with_emotion

# 테스트 데이터 준비
with open("/app/test_novel.txt", 'r', encoding='utf-8') as f:
    test_data = f.read().split('\n\n---\n\n')

# 모델 훈련
logging.info("Starting model training...")
try:
    train_model(config)
    logging.info("Model training completed successfully.")
except Exception as e:
    logging.exception(f"Error during model training: {e}")

# 훈련된 모델을 사용한 테스트
from deeppavlov import build_model

model = build_model(config)

for i, story in enumerate(test_data):
    logging.info(f"Testing story {i+1}")
    sentences = story.split('.')[:5]  # 각 이야기의 처음 5문장만 사용
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            emotion = emotion_classifier(sentence)[0]['label']
            response = model([sentence])
            logging.info(f"Q: {sentence}")
            logging.info(f"Detected Emotion: {emotion}")
            logging.info(f"A: {response[0]}")
            logging.info("---")

logging.info("Test completed")