FROM python:3.13-slim AS builder

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python","-m","flask","--app","flaskapi.py","run","--host=0.0.0.0"]