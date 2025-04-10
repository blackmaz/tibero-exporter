FROM python:3.11-slim

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo "Asia/Seoul" > /etc/timezone

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# JAVA_HOME 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY requirements.txt .
RUN pip install distlib setuptools wheel && \
    pip install -r requirements.txt

COPY tibero /tibero
COPY exporter /exporter
COPY config /config
COPY lib /lib
COPY main.py .
COPY common.py .
COPY config.yaml .

ENV ENV=PRD
ENV ACCOUNT_NAME=huniverse

CMD ["python", "./main.py"]