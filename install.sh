#!/bin/bash

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

print_status "Начинаем установку Anomer Backend..."

# Проверяем наличие необходимых утилит
print_status "Проверяем наличие необходимых утилит..."

# Проверяем что uv установлен, иначе выход из скрипта
if ! command -v uv &> /dev/null; then
    print_error "uv не найден! Установите uv: brew install uv"
    exit 1
fi

# Проверяем что openssl установлен, иначе выход из скрипта
if ! command -v openssl &> /dev/null; then
    print_error "openssl не найден! Установите openssl"
    exit 1
fi

# Проверяем что docker установлен, иначе выход из скрипта
if ! command -v docker &> /dev/null; then
    print_warning "Docker не найден! Установите Docker Desktop для работы с базой данных"
fi

print_success "Все необходимые утилиты найдены"

# Создание директории certs
print_status "Создаем директорию для сертификатов..."
if [ ! -d "certs" ]; then
    mkdir -p certs
    print_success "Директория certs создана"
else
    print_warning "Директория certs уже существует"
fi

# Проверяем, существуют ли уже ключи
if [ -f "certs/jwt-private.pem" ] || [ -f "certs/jwt-public.pem" ]; then
    print_warning "Сертификаты уже существуют в директории certs/"
    read -p "Хотите пересоздать сертификаты? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Удаляем старые сертификаты..."
        rm -f certs/jwt-private.pem certs/jwt-public.pem
    else
        print_status "Пропускаем создание сертификатов"
        goto_uv_sync=true
    fi
fi

# Выполняем создание новых сертификатов
if [ "$goto_uv_sync" != "true" ]; then
    # Генерация приватного ключа
    print_status "Генерируем приватный RSA ключ..."
    if openssl genrsa -out certs/jwt-private.pem 2048; then
        print_success "Приватный ключ создан: certs/jwt-private.pem"
    else
        print_error "Ошибка при создании приватного ключа"
        exit 1
    fi

    # Получение публичного ключа
    print_status "Создаем публичный ключ..."
    if openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem; then
        print_success "Публичный ключ создан: certs/jwt-public.pem"
    else
        print_error "Ошибка при создании публичного ключа"
        exit 1
    fi

    # Устанавливаем правильные права доступа
    chmod 600 certs/jwt-private.pem
    chmod 644 certs/jwt-public.pem
    print_success "Права доступа к сертификатам установлены"
fi

# Проверяем наличие .env файла
# Копируем .env.example в .env (при клонировании файла .env нет)
if [ ! -f ".env" ]; then
    print_warning "Файл .env не найден!"
    print_status "Создаем файл .env с настройками окружения..."
    if cp .env.example .env; then
        print_success "Файл .env создан успешно из .env.example"
    else
        print_error "Ошибка при создании файла .env"
        print_error "Убедитесь, что файл .env.example существует"
        exit 1
    fi
    echo ""
fi

# Инициализация проекта
print_status "Инициализируем проект с помощью uv..."
if uv sync; then
    print_success "Зависимости установлены успешно"
else
    print_error "Ошибка при установке зависимостей"
    exit 1
fi

print_status "Проверяем и устанавливаем права доступа для скриптов..."

# Список скриптов для проверки
scripts=("alembic.sh" "scripts/create_env_example.sh")

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ ! -x "$script" ]; then
            print_status "Устанавливаем права на выполнение для $script..."
            if chmod +x "$script"; then
                print_success "Права доступа установлены для $script"
            else
                print_error "Ошибка при установке прав доступа для $script"
                exit 1
            fi
        else
            print_success "$script уже имеет права на выполнение"
        fi
    else
        print_warning "Скрипт $script не найден"
    fi
done

# При клонировании у юзера нет файла redis.conf, поэтому генерируем его из файла redis.conf.example
print_status "Создаем redis.conf..."
if python3 scripts/replacer.py .env redis.conf.example -o redis.conf; then
    print_success "redis.conf создан успешно"
else
    print_error "Ошибка при создании redis.conf"
    exit 1
fi

# Создаем docker-compose.yml
print_status "Создаем docker-compose.yml..."
if python3 scripts/replacer.py .env docker-compose.example.yml -o docker-compose.yml; then
    print_success "docker-compose.yml создан успешно"
else
    print_error "Ошибка при создании docker-compose.yml"
    exit 1
fi

print_success "Установка завершена!"
echo ""
print_status "Следующие шаги:"
echo "1. Заполните параметры в файле .env"
echo "2. Запустите Postgres и Redis: docker-compose up pg redis -d --build"
echo "3. Примените миграции: ./alembic.sh upgrade head"
echo "4. Запустите сервер: uv run main.py"
