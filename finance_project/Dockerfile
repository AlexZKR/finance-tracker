FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN ["pip", "install", "-r", "./requirements.txt", "--no-cache-dir"]
COPY . .
RUN useradd app
USER app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]