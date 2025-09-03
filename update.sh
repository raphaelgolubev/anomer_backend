#!/bin/bash

# TODO: спрашивать у юзера, хочет ли он выполнить uv sync

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверяем, что мы в корневой директории проекта
if [ ! -f "pyproject.toml" ]; then
    print_error "Скрипт должен быть запущен из корневой директории проекта!"
    print_error "Убедитесь, что файл pyproject.toml находится в текущей директории."
    exit 1
fi

# Обновляем redis.conf
print_status "Обновляем redis.conf..."
if python3 scripts/replacer.py .env redis.conf.example -o redis.conf; then
    print_success "redis.conf обновлен успешно"
else
    print_error "Ошибка при создании redis.conf"
    exit 1
fi

# Обновляем docker-compose.yml
print_status "Обновляем docker-compose.yml..."
if python3 scripts/replacer.py .env docker-compose.example.yml -o docker-compose.yml; then
    print_success "docker-compose.yml обновлен успешно"
else
    print_error "Ошибка при создании docker-compose.yml"
    exit 1
fi