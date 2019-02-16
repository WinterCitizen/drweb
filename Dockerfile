FROM python:3.7-alpine
WORKDIR /app/src
COPY drweb/* ./
COPY ./requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
