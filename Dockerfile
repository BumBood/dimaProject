FROM python:3.12-alpine3.22

WORKDIR /app

# Установка зависимостей для сборки пакетов
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    && rm -rf /var/cache/apk/*

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Установка рабочей директории на src, где находятся все модули
WORKDIR /app/src

# Открытие порта для приложения
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]