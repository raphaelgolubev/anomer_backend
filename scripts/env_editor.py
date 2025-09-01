#!/usr/bin/env python3
"""
CLI инструмент для редактирования .env файлов
Поддерживает добавление параметров, секций и переименование секций
"""

import argparse
import re
import sys
import os
from typing import Optional


class EnvFileEditor:
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.lines = []
        self.load_file()

    def load_file(self):
        """Загружает содержимое .env файла"""
        if os.path.exists(self.env_file):
            with open(self.env_file, "r", encoding="utf-8") as f:
                self.lines = f.readlines()
        else:
            self.lines = []

    def save_file(self):
        """Сохраняет изменения в .env файл"""
        with open(self.env_file, "w", encoding="utf-8") as f:
            f.writelines(self.lines)

    def find_section(self, section_name: str) -> Optional[int]:
        """Находит индекс строки с секцией"""
        for i, line in enumerate(self.lines):
            if re.match(rf"^\s*#\s*---\s+{re.escape(section_name)}\s*$", line.strip()):
                return i
        return None

    def find_section_end(self, section_start: int) -> int:
        """Находит конец секции (следующая секция или конец файла)"""
        for i in range(section_start + 1, len(self.lines)):
            line = self.lines[i].strip()
            if line.startswith("# ---"):
                return i - 1
        return len(self.lines)

    def find_param(self, name: str) -> int:
        """
        Находит параметр и возвращает его индекс, если есть.
        Возвращает -1, если параметр не найден.
        """
        for i, line in enumerate(self.lines):
            if name.lower() in line.lower():
                return i
        return -1

    def _is_numeric(self, value: str) -> bool:
        """Проверяет, является ли значение числовым"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_boolean(self, value: str) -> bool:
        """Проверяет, является ли значение булевым"""
        return value.lower() in ("true", "false", "yes", "no", "on", "off", "1", "0")

    def _is_list(self, value: str) -> bool:
        """Проверяет, является ли значение списком"""
        return value.startswith("[") and value.endswith("]")

    def _should_quote(self, value: str) -> bool:
        """Определяет, нужно ли заключать значение в кавычки"""
        # Не заключаем в кавычки числовые и булевы значения, списки
        return not (
            self._is_numeric(value) or self._is_boolean(value) or self._is_list(value)
        )

    def _validate_param_name(self, param_name: str) -> None:
        """Проверяет, что параметр имеет префикс секции"""
        if "_" not in param_name:
            raise ValueError(
                f"Все параметры должны иметь префикс секции, например 'SERVER_DEBUG', где 'SERVER_' это префикс с названием секции"
            )

    def _get_section_from_param(self, param_name: str) -> str:
        """Определяет название секции на основе префикса параметра"""
        self._validate_param_name(param_name)

        # Извлекаем префикс (часть до первого подчеркивания)
        prefix = param_name.split("_")[0]

        # Преобразуем префикс в название секции
        # Например: SERVER -> Server, ENABLE -> Enable, APP -> App
        section_name = prefix.capitalize()

        return section_name

    def add_section(self, section_name: str):
        """Добавляет новую секцию в конец файла"""
        # Добавляем пустую строку перед секцией, если файл не пустой
        if self.lines:
            # Убеждаемся, что последняя строка заканчивается символом новой строки
            if self.lines[-1] and not self.lines[-1].endswith("\n"):
                self.lines[-1] += "\n"
            # Добавляем пустую строку перед секцией
            self.lines.append("\n")

        # Добавляем секцию
        self.lines.append(f"# --- {section_name}\n")
        print(f"Секция '{section_name}' добавлена")

    def add_param_to_section(
        self,
        section_name: str,
        param_name: str,
        param_value: str,
        description: str = None,
    ):
        """Добавляет параметр в указанную секцию"""

        # проверяем есть ли параметр
        exists_param_index = self.find_param(param_name)
        if exists_param_index != -1:
            print(f"Параметр {param_name} уже существует! Перезаписываем...")

            if (
                "<" in self.lines[exists_param_index - 1]
                and ">" in self.lines[exists_param_index - 1]
            ):
                # удаляем сначала комментарий над параметром
                self.lines.pop(exists_param_index - 1)
                # удаляем сам параметр
                self.lines.pop(exists_param_index - 1)
            else:
                # удаляем параметр
                self.lines.pop(exists_param_index)

        section_index = self.find_section(section_name)

        if section_index is None:
            # Создаем секцию, если её нет
            self.add_section(section_name)
            section_index = len(self.lines) - 1

        # Находим конец секции
        section_end = self.find_section_end(section_index)

        # Формируем строки для добавления
        new_lines = []

        if description:
            # Добавляем комментарий с описанием
            if self._should_quote(param_value):
                comment_value = (
                    f'"{param_value}"'
                    if not param_value.startswith('"')
                    else param_value
                )
            else:
                comment_value = param_value
            new_lines.append(f"    # <{comment_value}> - {description}\n")

        # Добавляем параметр
        if self._should_quote(param_value):
            param_value_formatted = (
                f'"{param_value}"' if not param_value.startswith('"') else param_value
            )
        else:
            param_value_formatted = param_value
        new_lines.append(f"    {param_name.upper()}={param_value_formatted}\n")

        # Вставляем строки в конец секции
        self.lines[section_end:section_end] = new_lines

        print(f"Параметр '{param_name.upper()}' добавлен в секцию '{section_name}'")

    def add_param(self, param_name: str, param_value: str, description: str = None):
        """Добавляет параметр в соответствующую секцию на основе префикса"""
        # Определяем секцию на основе префикса параметра
        section_name = self._get_section_from_param(param_name)
        self.add_param_to_section(section_name, param_name, param_value, description)

    def rename_section(self, old_name: str, new_name: str):
        """Переименовывает секцию и все параметры с соответствующим префиксом"""
        section_index = self.find_section(old_name)

        if section_index is None:
            print(f"Секция '{old_name}' не найдена")
            return

        # Переименовываем заголовок секции
        self.lines[section_index] = f"# --- {new_name}\n"

        # Находим конец секции
        section_end = self.find_section_end(section_index)

        # Переименовываем параметры с префиксом
        old_prefix = old_name.upper() + "_"
        new_prefix = new_name.upper() + "_"

        renamed_count = 0
        for i in range(section_index + 1, section_end):
            line = self.lines[i]
            if line.strip() and not line.strip().startswith("#"):
                # Проверяем, является ли строка параметром
                match = re.match(r"^(\s*)([A-Z_][A-Z0-9_]*)=(.*)$", line)
                if match:
                    indent, param_name, param_value = match.groups()
                    if param_name.startswith(old_prefix):
                        new_param_name = param_name.replace(old_prefix, new_prefix, 1)
                        # Сохраняем символ новой строки, если он был
                        line_ending = "\n" if line.endswith("\n") else ""
                        self.lines[i] = (
                            f"{indent}{new_param_name}={param_value}{line_ending}"
                        )
                        renamed_count += 1

        print(f"Секция '{old_name}' переименована в '{new_name}'")
        if renamed_count > 0:
            print(
                f"Переименовано {renamed_count} параметров с префиксом {old_prefix} на {new_prefix}"
            )

    def remove_param(self, param_name: str):
        """Удаляет параметр из файла"""
        param_index = self.find_param(param_name)
        if param_index != -1:
            if (
                "<" in self.lines[param_index - 1]
                and ">" in self.lines[param_index - 1]
            ):
                # удаляем комментарий над параметром
                self.lines.pop(param_index - 1)
                # удаляем сам параметр
                self.lines.pop(param_index - 1)
            else:
                # удаляем параметр
                self.lines.pop(param_index)
            print(f"Параметр '{param_name}' удален")
        else:
            print(f"Параметр '{param_name}' не найден")

    def remove_section(self, section_name: str):
        """Удаляет секцию из файла"""
        section_index = self.find_section(section_name)
        section_end = self.find_section_end(section_index)
        if section_index is not None:
            # удаляем секцию
            i = section_index
            while i != section_end + 1:
                # поскольку при удалении индексы сдвигаются, используем константу
                self.lines.pop(section_index)
                i += 1

            print(f"Секция '{section_name}' удалена")
        else:
            print(f"Секция '{section_name}' не найдена")


def main():
    parser = argparse.ArgumentParser(
        description="CLI инструмент для редактирования .env файлов"
    )
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда add param
    add_param_parser = subparsers.add_parser("add", help="Добавить параметр или секцию")
    add_param_parser.add_argument(
        "type", choices=["param", "section"], help="Тип добавляемого элемента"
    )
    add_param_parser.add_argument("name", help="Имя параметра или секции")
    add_param_parser.add_argument("value", nargs="?", help="Значение параметра")
    add_param_parser.add_argument("-d", "--description", help="Описание параметра")
    add_param_parser.add_argument(
        "-s",
        "--section",
        help="Секция для добавления параметра (определяется автоматически по префиксу)",
    )

    # Команда rename section
    rename_parser = subparsers.add_parser("rename", help="Переименовать секцию")
    rename_parser.add_argument("type", choices=["section"], help="Тип переименования")
    rename_parser.add_argument("old_name", help="Старое имя секции")
    rename_parser.add_argument("to", help='Слово "to"')
    rename_parser.add_argument("new_name", help="Новое имя секции")

    # Команда remove
    remove_parser = subparsers.add_parser("remove", help="Удалить параметр или секцию")
    remove_parser.add_argument(
        "type", choices=["param", "section"], help="Тип удаляемого элемента"
    )
    remove_parser.add_argument("name", help="Имя параметра или секции")

    # Общие аргументы
    parser.add_argument("-f", "--file", default=".env", help="Путь к .env файлу")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    editor = EnvFileEditor(args.file)

    try:
        if args.command == "add":
            if args.type == "param":
                if not args.value:
                    print("Ошибка: для параметра необходимо указать значение")
                    return
                if args.section:
                    # Если секция указана явно, используем её
                    editor.add_param_to_section(
                        args.section, args.name, args.value, args.description
                    )
                else:
                    # Если секция не указана, определяем её по префиксу параметра
                    editor.add_param(args.name, args.value, args.description)
            elif args.type == "section":
                editor.add_section(args.name)

        elif args.command == "rename":
            if args.type == "section":
                if args.to.lower() != "to":
                    print("Ошибка: используйте 'to' между старым и новым именем")
                    return
                editor.rename_section(args.old_name, args.new_name)

        elif args.command == "remove":
            if args.type == "param":
                editor.remove_param(args.name)
            elif args.type == "section":
                editor.remove_section(args.name)

        editor.save_file()
        print(f"Изменения сохранены в файл {args.file}")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
