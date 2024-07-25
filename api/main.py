import os
import json
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from deeppavlov import build_model
from deeppavlov.core.commands.utils import parse_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

logger.info(f"DOWNLOADS_PATH: {downloads_path}")

with open("/app/deep_pavlov_config.json", "r") as config_file:
    config = json.load(config_file)

config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

logger.info("Building intent classification model...")
intent_model = build_model(config, download=False)
logger.info("Intent classification model built successfully.")

# 훈련 데이터 로드
with open('/app/combined_data.txt', 'r', encoding='utf-8') as f:
    response_data = f.read().split('\n\n---\n\n')

# TF-IDF 벡터라이저 초기화 및 훈련
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(response_data)

def generate_response(text):
    # 입력 텍스트를 TF-IDF 벡터로 변환
    text_vector = vectorizer.transform([text])
    
    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(text_vector, tfidf_matrix).flatten()
    
    # 가장 유사한 응답의 인덱스
    most_similar_idx = cosine_similarities.argsort()[-1]
    
    # 가장 유사한 응답 반환
    response = response_data[most_similar_idx]
    
    # 응답이 너무 길 경우 적절히 자르기
    max_response_length = 200  # 최대 응답 길이 설정
    if len(response) > max_response_length:
        response = response[:max_response_length] + "..."
    
    return response

def predict_intent(text):
    return intent_model([text])[0]