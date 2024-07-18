FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DOWNLOADS_PATH=/app/downloads

# 시스템 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    ca-certificates \
    wget \
    gnupg \
    curl \
    unzip \
    libatlas-base-dev \
    libgomp1 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Python 3.8 설치
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8 python3.8-venv python3.8-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --set python3 /usr/bin/python3.8 && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriver 설치
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm ~/chromedriver_linux64.zip && \
    chmod 0755 /usr/local/bin/chromedriver

# Python 의존성 설치
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

# DOWNLOADS_PATH 디렉토리 생성
RUN mkdir -p $DOWNLOADS_PATH

# 애플리케이션 코드 복사
COPY api /app/api
COPY deep_pavlov_config.json /app/

WORKDIR /app

CMD DOWNLOADS_PATH=$DOWNLOADS_PATH python3 api/main.py