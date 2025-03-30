FROM python:3.9-slim

RUN apt update
RUN apt install -y python3-pip
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY src /app/src
WORKDIR /app/src

ENV PYTHONPATH="/app/src"

EXPOSE 8000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "app:app"]