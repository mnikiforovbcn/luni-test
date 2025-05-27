# === BUILD STAGE ===
FROM python:3.11-slim AS builder

WORKDIR /app

# Кэшируем зависимости
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === RUN STAGE ===
FROM python:3.11-slim

# Добавляем локальные пакеты в PATH
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Переносим зависимости
COPY --from=builder /root/.local /root/.local

# Копируем приложение
COPY main.py .
COPY frontend/ ./frontend/

# Открываем HTTP-порт
EXPOSE 80

# Запуск Flask-сервера
CMD ["python", "main.py"]
