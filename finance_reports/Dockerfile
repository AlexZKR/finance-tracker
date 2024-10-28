FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN ["pip", "install", "-r", "./requirements.txt", "--no-cache-dir"]
COPY . .
RUN useradd app
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]