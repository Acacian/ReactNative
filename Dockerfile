# 베이스 이미지로 Ubuntu 20.04를 사용
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libatlas-base-dev \
    libgomp1 \
    curl \
    xvfb \
    gnupg

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable

# Install chromedriver
RUN wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/

# Set display port to avoid crash
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY api /app/api
COPY deep_pavlov_config.json /app/deep_pavlov_config.json

# Set the command to run the application
CMD ["python3", "/app/api/main.py"]
