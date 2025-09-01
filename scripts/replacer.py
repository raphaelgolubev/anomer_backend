#!/usr/bin/env python3
# Скрипт заменяет вхождения *{VAR} в файле значениями из .env
# Поддерживает кавычки, пробелы и простые комментарии в .env

import re
import sys
import argparse
from pathlib import Path


# Разбор .env файла: поддерживаются строки вида
# KEY=VALUE, KEY="value", KEY='value'
# Игнорируются пустые строки и строки, начинающиеся с #
def parse_env(path: Path):
    env = {}
    line_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
    if not path.exists():
        raise FileNotFoundError(f".env файл не найден: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            # пропустить пустые или комментарии
            continue
        m = line_re.match(raw)
        if not m:
            # некорректная строка — пропустить
            continue
        key, val = m.group(1), m.group(2).strip()
        # если значение в кавычках — убрать их
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            val = val[1:-1]
        else:
            # удалить inline-комментарий вида " ... # comment"
            comment_idx = val.find(" #")
            if comment_idx != -1:
                val = val[:comment_idx].rstrip()
            # на случай, если остались случайные кавычки вокруг
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
        env[key] = val
    return env


# Замена шаблонов вида *{VAR} на значение из env
# Поддерживается только точное совпадение символа '*' перед '{'
def replace_placeholders(text: str, env: dict):
    # Паттерн ищет '*' непосредственно перед '{' и захватывает имя переменной
    pattern = re.compile(r"\*\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def repl(m):
        name = m.group(1)
        # Если переменная найдена в env — вернуть её значение, иначе вернуть исходный текст (оставляем "*{VAR}")
        return env.get(name, m.group(0))

    return pattern.sub(repl, text)


def main():
    # Аргументы командной строки на русском языке в помощи
    parser = argparse.ArgumentParser(
        description="Заменяет *{VAR} в файле значениями из .env"
    )
    parser.add_argument("envfile", type=Path, help="путь до .env файла")
    parser.add_argument("target", type=Path, help="обрабатываемый файл")
    parser.add_argument(
        "-o", "--output", type=Path, help="путь для сохранения результата"
    )
    parser.add_argument(
        "--inplace", action="store_true", help="перезаписать целевой файл"
    )
    args = parser.parse_args()

    # Проверка конфликтующих опций
    if args.inplace and args.output:
        print(
            "Ошибка: указаны и --inplace, и -o/--output; выберите только один вариант.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Чтение .env
    try:
        env = parse_env(args.envfile)
    except Exception as e:
        print(f"Ошибка при чтении .env: {e}", file=sys.stderr)
        sys.exit(2)

    # Проверка наличия целевого файла
    if not args.target.exists():
        print(f"Целевой файл не найден: {args.target}", file=sys.stderr)
        sys.exit(3)

    # Чтение, замена и вывод/сохранение результата
    text = args.target.read_text(encoding="utf-8")
    new_text = replace_placeholders(text, env)

    if args.inplace:
        # Перезаписать целевой файл
        args.target.write_text(new_text, encoding="utf-8")
    elif args.output:
        # Создать директорию при необходимости и записать в указанный файл
        outp = args.output
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(new_text, encoding="utf-8")
    else:
        # Вывести в stdout
        print(new_text)


if __name__ == "__main__":
    main()
