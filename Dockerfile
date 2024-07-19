FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DOWNLOADS_PATH=/app/downloads
ENV CHROME_VERSION="google-chrome-stable"
ENV CHROMEDRIVER_DIR=/usr/local/bin/chromedriver
ENV CHROME_SETUP=google-chrome.deb

# 시스템 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    wget curl unzip gnupg software-properties-common \
    apt-transport-https ca-certificates libatlas-base-dev \
    libgomp1 xvfb python3.8 python3.8-venv python3.8-dev python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 설정
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --set python3 /usr/bin/python3.8 && \
    python3 -m pip install --upgrade pip

# Google Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y ${CHROME_VERSION} && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ChromeDriver 설치 (여러 방법 시도)
RUN CHROME_VERSION=$(google-chrome --version | awk '{ print $3 }' | awk -F'.' '{ print $1 }') \
    && CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) \
    && wget -N http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ${CHROMEDRIVER_DIR} \
    && rm ~/chromedriver_linux64.zip \
    && chmod +x ${CHROMEDRIVER_DIR}/chromedriver \
    || (apt-get update && apt-get install -y chromium-chromedriver) \
    || (pip install webdriver-manager)

# Python 의존성 설치
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

# DOWNLOADS_PATH 디렉토리 생성
RUN mkdir -p $DOWNLOADS_PATH

# 애플리케이션 코드 복사
COPY api /app/api
COPY deep_pavlov_config.json /app/

WORKDIR /app

# Chrome 및 ChromeDriver 버전 확인
RUN echo "Chrome version:" && google-chrome --version && \
    echo "ChromeDriver version:" && chromedriver --version || echo "ChromeDriver not found"

# 데이터 수집 및 모델 훈련
RUN python3 api/data_collection.py || (cat /app/data_collection.log && exit 1)
RUN python3 api/train_model.py

CMD ["python3", "api/main.py"]