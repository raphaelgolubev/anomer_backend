# Anomer backend
<p align="left">
  <img src="docs/logo.svg" alt="Project Logo" width="120" height="120">
</p>

**A***nother* **N***ew* **O***nline* **ME***ssenge***R**

- Python 3.12.3+
- FastAPI

# Установка

## MacOS
### Подготовка к установке
>Примечание: команды ниже необходимо выполнять в терминале (bash или другая shell оболочка). Убедитесь, что у вас есть утилита `git` и она корректно настроена: см. [Установка Git](https://www.w3schools.com/git/git_install.asp?remote=github) и [Git&Github. Начало работы](https://www.w3schools.com/git/git_remote_getstarted.asp?remote=github)

>ВАЖНО: в проекте используется пакетный менеджер [`uv`](https://habr.com/ru/companies/otus/articles/903578/) вместо `pip`. Рекомендую установить его с помощью [`Homebrew`](https://brew.sh/):

Установите `Homebrew`:
  ```shell
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
Затем установите `uv`:
  ```shell
  brew install uv
  ```

### Автоматическая установка

1. Клонируйте репозиторий и перейдите в корневую директорию проекта:
```shell
git clone https://github.com/raphaelgolubev/anomer_backend.git && cd anomer_backend
```

2. Запустите автоматический скрипт установки:
```shell
chmod +x install.sh && ./install.sh
```

Скрипт автоматически:
- ✅ Проверит наличие необходимых утилит
- ✅ Создаст директорию `certs` и сгенерирует RSA ключи
- ✅ Установит зависимости проекта
- ✅ Покажет инструкции по настройке `.env` файла

### Ручная установка (альтернатива)

Если вы предпочитаете ручную установку:

1. Создайте папку для хранения сертификатов `certs`:
```shell
mkdir certs
```

2. Сгенерируйте приватный ключ (RSA):
```shell
openssl genrsa -out certs/jwt-private.pem 2048
```

3. Получите публичный ключ:
```shell
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```

4. Установите [`Docker Desktop`](https://docs.docker.com/desktop/setup/install/mac-install/) и запустите его.

5. Инициализируйте проект:
```shell
uv sync
```

### Настройка окружения

Скопируйте файл `.env.example` в `.env`:
```shell
cp .env.example .env
```

Отредактируйте файл `.env` и замените значения на ваши:
```shell
nano .env
# или
code .env
# или любой другой текстовый редактор
```

>ВНИМАНИЕ: Не храните эти файлы и их содержание в публичном доступе! Файлы с расширением `*.pem` внесены в `.gitignore`, чтобы запретить их отслеживание системами контроля версий, в данном случае `Git`.

### Запуск

1. Запустите базу данных:
```shell
docker-compose up pg -d --build
```
Эта команда скачает образ `PostgreSQL` и запустит контейнер в фоновом режиме.

2. Выполните миграцию:
```shell
chmod +x alembic.sh && ./alembic.sh upgrade head
```

3. Запустите сервер:
```shell
uv run main.py
```
Эта команда запустит локальный сервер по адресу http://0.0.0.0:8001

>ПРИМЕЧАНИЕ: Убедитесь, что в файле `.env` правильно настроены все переменные окружения, особенно настройки базы данных и почты.

## Linux
```python
raise NotImplementedError
```

## Windows
Просто не используйте винду :)

# License

GNU AGPLv3