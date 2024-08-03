FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DOWNLOADS_PATH=/app/downloads
ENV CHROME_VERSION="google-chrome-stable"
ENV CHROMEDRIVER_DIR=/usr/local/bin
ENV CHROME_SETUP=google-chrome.deb
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV DISPLAY=:99

# 시스템 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    wget curl unzip gnupg software-properties-common \
    apt-transport-https ca-certificates libatlas-base-dev \
    libgomp1 xvfb python3.8 python3.8-venv python3.8-dev python3-pip \
    dnsutils \
    libnss3 libgconf-2-4 libfontconfig1 libatk-bridge2.0-0 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 설정
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --set python3 /usr/bin/python3.8 && \
    python3 -m pip install --upgrade pip setuptools wheel

# Google Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

# DOWNLOADS_PATH 디렉토리 생성
RUN mkdir -p $DOWNLOADS_PATH

# 애플리케이션 코드 복사
COPY api /app/api
COPY deep_pavlov_config.json /app/
COPY Korean_SNS_DATA /app/Korean_SNS_DATA

WORKDIR /app

# Chrome 버전 확인
RUN echo "Chrome version:" && google-chrome --version

# 데이터 수집, 마이닝 및 모델 훈련
RUN Xvfb :99 -ac & \
    python3 api/data_collection.py | tee /app/data_collection.log || (cat /app/data_collection.log && exit 1)
RUN python3 api/data_mining.py | tee /app/data_mining.log || (cat /app/data_mining.log && exit 1)
RUN python3 api/train_model.py

# 포트 노출
EXPOSE 5000

# API 서버 실행
CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000"]