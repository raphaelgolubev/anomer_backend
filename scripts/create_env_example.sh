#!/bin/bash

# Скрипт для создания .env.example из .env файла
# Использует значения из угловых скобок в комментариях для создания примера

# Проверяем наличие аргумента с путем к .env файлу
if [ $# -eq 0 ]; then
    echo "Использование: $0 <путь_к_env_файлу>"
    echo "Пример: $0 .env"
    exit 1
fi

ENV_FILE="$1"
EXAMPLE_FILE=".env.example"

# Проверяем существование исходного файла
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Ошибка: Файл '$ENV_FILE' не найден"
    exit 1
fi

# Создаем временный файл для обработки
TEMP_FILE=$(mktemp)

# Обрабатываем файл построчно
while IFS= read -r line; do
    # Если строка содержит комментарий с угловыми скобками
    if [[ $line =~ ^[[:space:]]*#.*\<.*\>.*-.*$ ]]; then
        # Извлекаем значение из угловых скобок
        if [[ $line =~ \<([^>]+)\> ]]; then
            example_value="${BASH_REMATCH[1]}"
            # Создаем комментарий с примером, заменяя содержимое угловых скобок
            new_line=$(echo "$line" | sed "s|<[^>]*>|<${example_value}>|")
            echo "$new_line" >> "$TEMP_FILE"
        else
            echo "$line" >> "$TEMP_FILE"
        fi
    # Если строка содержит переменную окружения
    elif [[ $line =~ ^[[:space:]]*[A-Z_][A-Z0-9_]*= ]]; then
        # Ищем предыдущий комментарий с угловыми скобками
        # Читаем предыдущие строки из временного файла
        prev_comment=""
        if [ -f "$TEMP_FILE" ]; then
            prev_comment=$(tail -1 "$TEMP_FILE" 2>/dev/null)
        fi
        
        # Если предыдущий комментарий содержит угловые скобки
        if [[ $prev_comment =~ \<([^>]+)\> ]]; then
            example_value="${BASH_REMATCH[1]}"
            # Извлекаем имя переменной и отступы
            var_name=$(echo "$line" | cut -d'=' -f1)
            # Проверяем, нужно ли добавить кавычки (если в исходном значении они были)
            original_value=$(echo "$line" | cut -d'=' -f2-)
            if [[ $original_value =~ ^\".*\"$ ]]; then
                # Если исходное значение было в кавычках, используем значение из угловых скобок как есть
                echo "${var_name}=${example_value}" >> "$TEMP_FILE"
            else
                # Иначе используем значение без кавычек
                echo "${var_name}=${example_value}" >> "$TEMP_FILE"
            fi
        else
            echo "$line" >> "$TEMP_FILE"
        fi
    else
        # Обычные строки (секции, пустые строки и т.д.)
        echo "$line" >> "$TEMP_FILE"
    fi
done < "$ENV_FILE"

# Перемещаем результат в финальный файл
mv "$TEMP_FILE" "$EXAMPLE_FILE"

echo "✅ Файл .env.example успешно создан на основе $ENV_FILE"