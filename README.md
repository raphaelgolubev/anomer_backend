# Anomer backend
<p align="left">
  <img src="docs/logo.svg" alt="Project Logo" width="120" height="120">
</p>

**A***nother* **N***ew* **O***nline* **ME***ssenge***R**

- python 3.12.3+
- fastapi

# Установка

## MacOS
### Подготовка к установке
>Примечание: команды ниже необходимо выполнять в терминале (bash или другая shell оболочка). Убедитесь, что у вас есть утилита `git` и она корректно настроена: см. [Установка Git](https://www.w3schools.com/git/git_install.asp?remote=github) и [Git&Github. Начало работы](https://www.w3schools.com/git/git_remote_getstarted.asp?remote=github)

>ВАЖНО: в проекте используется пакетный менеджер [`uv`](https://habr.com/ru/companies/otus/articles/903578/) вместо `pip`. Рекомендую установить его с помощью [`Homebrew`](https://brew.sh/):

Установите `Homebrew`:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
Затем установите `uv`:
  ```bash
  brew install uv
  ```
----
1. Клонируйте репозиторий и перейдите в корневую директорию проекта:
```bash
git clone https://github.com/raphaelgolubev/anomer_backend.git && cd anomer_backend
```
Первая команда скачает весь исходный код из удаленного репозитория, вторая команда перейдет в корневую директорию проекта.

2. Создайте папку для хранения сертификатов `certs`:
```bash
mkdir certs
```
Эта команда создаст директорию `certs` в том месте, откуда она была вызвана.

3. Сгенерируйте приватный ключ (RSA):
```bash
openssl genrsa -out certs/jwt-private.pem 2048
```
Эта команда создаст файл с приватным ключом (сертификат) `jwt-private.pem` в директории `certs`.

4. Теперь нужно получить публичный ключ:
```bash
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```
Эта команда создаст файл с публичным ключом в том же месте.

>ВНИМАНИЕ: Не храните эти файлы и их содержание в публичном доступе! Файлы с расширением `*.pem` внесены в `.gitignore`, чтобы запретить их отслеживание системами контроля версий, в данном случае `Git`. 

5. Установите [`Docker Desktop`](https://docs.docker.com/desktop/setup/install/mac-install/) и запустите его.

6. Инициализируйте проект:
```bash
uv sync
```
Команда создаст виртуальное окружение и установит зависимости.

### Запуск

1. Не выходя из терминала, выполните в нем следующую команду:
```bash
docker-compose up pg -d --build
```
Эта команда скачает образ `PostgreSQL` и запустит контейнер в фоновом режиме.

2. Запустите сервер:
```bash
uv run main.py
```
Эта команда запустит локальный сервер по адресу http://0.0.0.0:8001

## Windows
Просто не используйте винду :)

# License

GNU AGPLv3