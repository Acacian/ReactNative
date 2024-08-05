import os
import logging
import numpy as np
from scikit-learn.feature_extraction.text import TfidfVectorizer
from scikit-learn.cluster import KMeans
from scikit-learn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.utils.data import DataLoader, TensorDataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read().split('\n\n---\n\n')
    logging.info(f"Loaded {len(data)} items from {file_path}")
    return data

def preprocess_data(data):
    # 여기에 필요한 전처리 단계를 추가
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
        
        cluster_text = ' '.join(cluster_data)
        tfidf = vectorizer.transform([cluster_text])
        feature_names = vectorizer.get_feature_names_out()
        sorted_indices = np.argsort(tfidf.toarray()[0])[::-1]
        top_keywords = [feature_names[idx] for idx in sorted_indices[:10]]
        logging.info(f"Top keywords: {', '.join(top_keywords)}")

def prepare_emotion_data(data, labels):
    # 여기서 감정 레이블을 자동으로 할당하는 로직을 구현
    # 예를 들어, 클러스터별로 가장 빈번한 감정 단어를 기반으로 레이블 할당
    emotion_labels = ['joy', 'sadness', 'anger', 'fear', 'neutral']
    assigned_emotions = [emotion_labels[label % len(emotion_labels)] for label in labels]
    return list(zip(data, assigned_emotions))

def train_emotion_classifier(data_with_emotions):
    texts, emotions = zip(*data_with_emotions)
    
    # BERT 토크나이저 및 모델 초기화
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(set(emotions)))

    # 데이터 인코딩
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors='pt')
    labels = torch.tensor([emotion_labels.index(e) for e in emotions])

    # 데이터셋 분할
    train_encodings, val_encodings, train_labels, val_labels = train_test_split(
        encodings['input_ids'], labels, test_size=0.2, random_state=42
    )

    # 데이터로더 생성
    train_dataset = TensorDataset(train_encodings, train_labels)
    val_dataset = TensorDataset(val_encodings, val_labels)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16)

    # 모델 훈련
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    for epoch in range(3):  # 3 에폭 동안 훈련
        model.train()
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids, labels = [b.to(device) for b in batch]
            outputs = model(input_ids, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

    # 모델 저장
    model.save_pretrained('/app/emotion_classifier')
    tokenizer.save_pretrained('/app/emotion_classifier')
    logging.info("Emotion classifier trained and saved.")

if __name__ == "__main__":
    data = load_data("/app/combined_data.txt")
    preprocessed_data = preprocess_data(data)
    
    labels, vectorizer = perform_clustering(preprocessed_data)
    analyze_clusters(preprocessed_data, labels, vectorizer)
    
    data_with_emotions = prepare_emotion_data(preprocessed_data, labels)
    train_emotion_classifier(data_with_emotions)
    
    logging.info("Data mining and emotion classifier training completed")