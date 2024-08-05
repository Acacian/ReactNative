# Python 3.9 이미지를 기반으로 합니다
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY data_mining.py train_model.py deep_pavlov_config.json ./
COPY test_novel.txt ./combined_data.txt

# 환경 변수 설정
ENV DOWNLOADS_PATH=/app/downloads

# 실행 명령
CMD ["python", "data_mining.py", "&&", "python", "train_model.py"]