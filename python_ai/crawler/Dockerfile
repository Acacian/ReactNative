FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DOWNLOADS_PATH=/app/downloads
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
    libgbm1 libasound2 libxshmfence1 libglu1-mesa libegl1-mesa \
    libpangocairo-1.0-0 libpango-1.0-0 libharfbuzz0b libgtk-3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 설정
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --set python3 /usr/bin/python3.8 && \
    python3 -m pip install --upgrade pip setuptools wheel

# Python 의존성 설치
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

# Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 애플리케이션 코드 복사
COPY *.py /app/
WORKDIR /app

# 데이터 수집을 위한 디렉토리 생성
RUN mkdir -p /app/downloads

# 데이터 수집 실행
RUN Xvfb :99 -ac & \
    python3 -u main.py > /app/crawling.log 2>&1 || (cat /app/crawling.log && exit 1)

# 크롤링 결과 확인
RUN ls -l /app/downloads && \
    if [ -f /app/downloads/combined_data.txt ]; then \
        echo "Crawling successful. Data file created."; \
        cat /app/crawling.log; \
    else \
        echo "Crawling failed. No data file found."; \
        cat /app/crawling.log; \
        exit 1; \
    fi

# 컨테이너 실행 시 기본 명령
CMD ["python3", "main.py"]