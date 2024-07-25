import os
import json
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deeppavlov import build_model
from deeppavlov.core.commands.utils import parse_config

logging.basicConfig(level=logging.INFO)

downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

logging.info(f"DOWNLOADS_PATH: {downloads_path}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("/app/deep_pavlov_config.json", "r") as config_file:
    config = json.load(config_file)

config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

logging.info("Building intent classification model...")
intent_model = build_model(config, download=False)
logging.info("Intent classification model built successfully.")

# 훈련 데이터 로드
with open('/app/combined_data.txt', 'r', encoding='utf-8') as f:
    response_data = f.read().split('\n\n---\n\n')

# TF-IDF 벡터라이저 초기화 및 훈련
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(response_data)

class Request(BaseModel):
    text: str

class Response(BaseModel):
    intent: str
    response: str

@app.post("/predict", response_model=Response)
def predict(request: Request):
    intent = intent_model([request.text])[0]
    
    response = generate_response(request.text)
    
    return Response(intent=intent, response=response)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)