# Установка

## Подготовка
### для любой системы
Прежде чем перейти к установке убедитесь, что:

- у вас установлен и настроен `git`: см. [Установка Git](https://www.w3schools.com/git/git_install.asp?remote=github) и [Git&Github. Начало работы](https://www.w3schools.com/git/git_remote_getstarted.asp?remote=github)

### для MacOS или Linux
- у вас установлен `Homebrew`, если нет, тогда установите его:

    ```shell
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

  <sub> `Homebrew` - это утилита командной строки в macOS и Linux, которая позволяет устанавливать пакеты и приложения. </sub>

- у вас установлен пакетный менеджер `uv`, если нет, тогда установите его с помощью `Homebrew`:

    ```shell
    brew install uv
    ```

  <sub> `uv` - это чрезвычайно быстрый пакетный менеджер Python, написанный на Rust. Разработан как замена для pip и pip-tools. Помимо этого он может собой заменить venv и pyenv. </sub>


> Примечание: Вы можете выбрать любой другой пакетный менеджер вместо `uv` и не устанавливать `Homebrew`, я ничего не навязываю, но туториал и скрипты написаны таким образом, что без этих утилит не обойтись. 

### для MacOS
- Установите [`Docker Desktop`](https://docs.docker.com/desktop/setup/install/mac-install/) и запустите его.

    <sub> Нажимте на "Docker Desktop" выше, чтобы перейти по ссылке для скачивания Docker Desktop. </sub>

### для Windows
- ~~установите Linux как вторую систему или купите макбук и не парьтесь~~ пока что этот раздел не готов.

## Скачайте репозиторий

1. Откройте терминал

2. В терминале перейдите в папку рабочего стола:
    ```shell
    cd Desktop
    ```

3. Клонируйте репозиторий:
    ```shell
    git clone https://github.com/raphaelgolubev/anomer_backend.git
    ```

    <sub> Команда скачает репозиторий в папку `"anomer_backend"` на вашем рабочем столе. </sub>

4. В терминале перейдите в папку проекта:
    ```shell
    cd anomer_backend
    ```

Выполните шаги ниже для вашей операционной системы:

## Автоматическая установка
Если вы хотите приложить минимум усилий:

### для MacOS или Linux
1. Находясь в папке anomer_backend в терминале, запустите автоматический скрипт установки:
    ```shell
    chmod +x install.sh && ./install.sh
    ```

    <sub> Команда `chmod +x install.sh` даст права на выполнение скрипта, команда `./install.sh` запустит сам скрипт. </sub>

Скрипт автоматически:
- ✅ Проверит наличие необходимых утилит
- ✅ Создаст директорию `certs` и сгенерирует RSA ключи
- ✅ Установит зависимости проекта
- ✅ Покажет инструкции по настройке `.env` файла
- ✅ Создаст файлы `redis.conf` и `docker-compose.yml`

> Примечание: в скрипте установки используется `replacer.py` - это простой шаблонзитор, который подставляет в произвольный файл значения из `.env файла`. Если вы изменили значения параметров в `.env`, то их необходимо снова применить для `redis.conf` и `docker-compose.yml`, для этого вам необходимо выполнить две команды:
-   для обновления `redis.conf`: 
    ```shell
    python3 scripts/replacer.py .env redis.conf.example -o redis.conf
    ```
-   для обновления `docker-compose.yml`: 
    ```shell
    python3 scripts/replacer.py .env docker-compose.example.yml -o docker-compose.yml
    ```

Готово! Теперь вы можете перейти непосредственно к [запуску проекта (нажмите сюда)](START.md)

Если возникли проблемы при установке, тогда попробуйте выполнить [ручную установку](#ручная-установка) или [найти решение здесь](TROUBLESHOOTING.md#проблемы-при-установке).

### для Windows
```python
raise NotImplementedError
```

## Ручная установка
Если вы предпочитате ручную установку или скрипт автоматической установки не сработал:

### для MacOS или Linux

1. Создайте папку для хранения сертификатов `certs`:

    ```shell
    mkdir certs
    ```

    <sub> Команда создаст папку `"certs"` в текущей директории. </sub>

2. Сгенерируйте приватный ключ (RSA):

    ```shell
    openssl genrsa -out certs/jwt-private.pem 2048
    ```

    <sub> Команда сгенерирует приватный ключ и сохранит его содержимое в папку "certs" в файл `"jwt-private.pem"`. </sub>

3. Получите публичный ключ:
    ```shell
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
    ```

    <sub> Команда сгенерирует публичный ключ и сохранит его содержимое в папку "certs" в файл `"jwt-public.pem"`. </sub>

4. Инициализируйте проект:
    ```shell
    uv sync
    ```

    <sub> Команда создаст виртуальное окружение в текущей директории, а также скачает и установит необходимые зависимости. </sub>

5. Создайте файл переменных окружения `.env`:
    ```shell
    cp .env.example .env
    ```

    <sub> Команда скопирует файл `.env.example` в новый файл `.env`  </sub>

6. Заполните параметры в файле `.env` своими значениями.

7. Предоставьте скриптам права на выполнение:
    ```shell
    chmod +x alembic.sh
    ```

    <sub> Скрипт `alembic.sh` это просто сокращение для команды `uv run python -m alembic -c alembic/alembic.ini`</sub>

8. Создайте `redis.conf`:
    ```shell
    python3 scripts/replacer.py .env redis.conf.example -o redis.conf
    ```

    <sub> Команда создаст файл `redis.conf` на основе значений параметров из `.env` </sub>

9. Создайте `docker-compose.yml`:
    ```shell
    python3 scripts/replacer.py .env docker-compose.example.yml -o docker-compose.yml
    ```

    <sub> Команда создаст файл `docker-compose.yml` на основе значений параметров из `.env` </sub>

> Примечание: скрипт `replacer.py` - это простой шаблонзитор, который подставляет в произвольный файл значения из `.env файла`. Если вы изменили значения параметров в `.env`, то их необходимо снова применить для `redis.conf` и `docker-compose.yml`, для этого выполните команды из пунктов 8 и 9 еще раз.

Готово! Теперь вы можете перейти непосредственно к [запуску проекта (нажмите сюда)](START.md). Если у вас возникли проблемы при установке, тогда попробуйте [найти решение проблемы здесь](TROUBLESHOOTING.md#проблемы-при-установке).

### для Windows

```python
raise NotImplementedError
```