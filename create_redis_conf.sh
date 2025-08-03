#!/bin/bash

# Создает redis.conf на основе redis.conf.example c заменой значения REDIS_PASSWORD из .env

# Проверяем, существует ли .env файл
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте файл .env с настройками окружения перед запуском этого скрипта."
    exit 1
fi

# Проверяем, существует ли redis.conf.example
if [ ! -f "redis.conf.example" ]; then
    echo "❌ Файл redis.conf.example не найден!"
    echo "Создайте файл redis.conf.example с настройками Redis перед запуском этого скрипта."
    exit 1
fi

# Чтение переменной из файла .env
REDIS_PASSWORD=$(grep -E '^[[:alnum:]_]+=' .env | grep '^REDIS_PASSWORD=' | sed 's/^REDIS_PASSWORD=//; s/#.*//; s/^"\(.*\)"$/\1/' | tr -d '"')

# Замена значения в redis.conf
cp redis.conf.example redis.conf
sed -i '' "s/requirepass .*/requirepass $REDIS_PASSWORD/" redis.conf

echo "✅ Redis конфигурация создана"