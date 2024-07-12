# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Python and necessary dependencies
RUN apt-get update && \
    apt-get install -y python3.8 python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install deeppavlov fastapi pydantic uvicorn

# Copy the current directory contents into the container at /app
COPY . .

# Copy DeepPavlov configuration file
COPY deep_pavlov_config.json /app/deeppavlov_config.json

# Expose ports for FastAPI server
EXPOSE 5000

# Command to start FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000"]
