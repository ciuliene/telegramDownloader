FROM python:3.12.1-slim-bullseye
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY src/*.py ./src/
COPY src/models/*.py ./src/models/
COPY .env .

CMD ["python", "main.py"]
