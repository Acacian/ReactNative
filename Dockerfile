# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install required dependencies and Python packages
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    software-properties-common \
    curl \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install Python packages
RUN pip install --upgrade pip && \
    pip install deeppavlov fastapi pydantic uvicorn torch transformers requests beautifulsoup4 selenium

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variables
ENV DOWNLOADS_PATH=/app/downloads

# Run data collection and training scripts
RUN python ./api/data_collection.py && \
    python ./api/train_model.py

# Expose ports for DeepPavlov server
EXPOSE 5000

# Command to start DeepPavlov server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000"]
