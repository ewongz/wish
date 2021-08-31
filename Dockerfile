FROM python:3.8
COPY src/ ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt