FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie as pastas mantendo a estrutura
COPY core/ ./core/
COPY sockets/ ./sockets/
COPY main.py .

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "main.py"]
