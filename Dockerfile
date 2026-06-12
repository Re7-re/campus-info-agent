# docker/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DEFAULT_AI_SERVICE=alibaba
ENV ALIBABA_API_KEY=""
ENV LOG_LEVEL=INFO

EXPOSE 7860
EXPOSE 8000

CMD ["python", "main.py", "--mode", "ui", "--port", "7860"]