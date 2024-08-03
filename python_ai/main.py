import os
import json
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from deeppavlov import build_model
from deeppavlov.core.commands.utils import parse_config
from data_mining import load_data, perform_clustering, analyze_clusters

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

downloads_path = os.getenv('DOWNLOADS_PATH', '/app/downloads')
os.environ['DOWNLOADS_PATH'] = downloads_path

logger.info(f"DOWNLOADS_PATH: {downloads_path}")

# 설정 파일 로드
try:
    with open("/app/deep_pavlov_config.json", "r") as config_file:
        config = json.load(config_file)
    logger.info("Configuration file loaded successfully.")
except FileNotFoundError:
    logger.error("deep_pavlov_config.json not found.")
    config = {}

config['dataset_reader']['data_path'] = config['dataset_reader']['data_path'].replace("{DOWNLOADS_PATH}", downloads_path)

# 의도 분류 모델 빌드
logger.info("Building intent classification model...")
try:
    intent_model = build_model(config, download=False)
    logger.info("Intent classification model built successfully.")
except Exception as e:
    logger.error(f"Error building intent model: {e}")
    intent_model = None

# 데이터 로드 및 클러스터링
data = load_data('/app/combined_data.txt')
labels, vectorizer = perform_clustering(data)
analyze_clusters(data, labels, vectorizer)

# TF-IDF 벡터라이저 초기화 및 훈련
tfidf_matrix = vectorizer.fit_transform(data)
logger.info("TF-IDF vectorization completed successfully.")
logger.info(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
logger.info(f"Top 10 words: {list(vectorizer.vocabulary_.keys())[:10]}")

def generate_response(text):
    if tfidf_matrix is None or len(data) == 0:
        return "죄송합니다. 응답을 생성할 수 없습니다."

    try:
        text_vector = vectorizer.transform([text])
        cosine_similarities = cosine_similarity(text_vector, tfidf_matrix).flatten()
        most_similar_idx = cosine_similarities.argsort()[-1]
        cluster_label = labels[most_similar_idx]
        
        # 같은 클러스터 내에서 가장 유사한 응답 선택
        cluster_indices = [i for i, label in enumerate(labels) if label == cluster_label]
        cluster_similarities = cosine_similarities[cluster_indices]
        most_similar_in_cluster = cluster_indices[cluster_similarities.argmax()]
        
        response = data[most_similar_in_cluster]
        
        max_response_length = 200
        if len(response) > max_response_length:
            response = response[:max_response_length] + "..."
        
        return response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "죄송합니다. 오류가 발생했습니다."

def predict_intent(text):
    if intent_model is None:
        return "intent_prediction_not_available"
    try:
        return intent_model([text])[0]
    except Exception as e:
        logger.error(f"Error predicting intent: {e}")
        return "intent_prediction_error"

# 모델 및 데이터 준비 상태 로깅
logger.info("Model and data preparation completed.")
logger.info(f"Number of responses available: {len(data)}")
logger.info(f"TF-IDF matrix shape: {tfidf_matrix.shape if tfidf_matrix is not None else 'Not available'}")
logger.info(f"Intent model available: {'Yes' if intent_model is not None else 'No'}")

if __name__ == "__main__":
    # 테스트 코드
    test_input = "안녕하세요"
    logger.info(f"Test input: {test_input}")
    logger.info(f"Generated response: {generate_response(test_input)}")
    logger.info(f"Predicted intent: {predict_intent(test_input)}")