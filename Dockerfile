FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv iputils-ping && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN python3 -m venv .venv
RUN . .venv/bin/activate && pip install -r requirements.txt

CMD ["bash", "-c", "source .venv/bin/activate && sh shells/launch.sh"]