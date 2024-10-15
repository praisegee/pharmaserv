FROM python:3.10-slim

#set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#set woking directory
WORKDIR /app

COPY requirements.txt .


RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn  # as the app server

COPY . .

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]