FROM python:3.10-slim

# Install dockerize
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64 -O /usr/local/bin/dockerize && \
    chmod +x /usr/local/bin/dockerize

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer.py .
ENTRYPOINT ["dockerize", "-wait", "http://api:8080/health", "-timeout", "60s", "python", "-u", "consumer.py"]
