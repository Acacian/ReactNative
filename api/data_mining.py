import os
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().split('\n\n---\n\n')
    logging.info(f"Loaded {len(data)} items from {file_path}")
    return data

def preprocess_data(data):
    # 여기에 필요한 전처리 단계를 추가할 수 있습니다.
    # 예: 불용어 제거, 특수문자 제거 등
    return data

def perform_clustering(data, n_clusters=5):
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(data)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    
    return kmeans.labels_, vectorizer

def analyze_clusters(data, labels, vectorizer):
    for i in range(max(labels) + 1):
        cluster_data = [data[j] for j in range(len(data)) if labels[j] == i]
        logging.info(f"Cluster {i}: {len(cluster_data)} items")
        
        # 클러스터의 주요 키워드 추출
        cluster_text = ' '.join(cluster_data)
        tfidf = vectorizer.transform([cluster_text])
        feature_names = vectorizer.get_feature_names_out()
        sorted_indices = np.argsort(tfidf.toarray()[0])[::-1]
        top_keywords = [feature_names[idx] for idx in sorted_indices[:10]]
        logging.info(f"Top keywords: {', '.join(top_keywords)}")

def extract_representative_samples(data, labels, n_samples=3):
    for i in range(max(labels) + 1):
        cluster_data = [data[j] for j in range(len(data)) if labels[j] == i]
        samples = random.sample(cluster_data, min(n_samples, len(cluster_data)))
        logging.info(f"Representative samples from Cluster {i}:")
        for sample in samples:
            logging.info(f"Sample: {sample[:100]}...")  # 처음 100자만 출력

if __name__ == "__main__":
    data = load_data("/app/combined_data.txt")
    preprocessed_data = preprocess_data(data)
    
    labels, vectorizer = perform_clustering(preprocessed_data)
    analyze_clusters(preprocessed_data, labels, vectorizer)
    extract_representative_samples(preprocessed_data, labels)
    
    logging.info("Data mining completed")