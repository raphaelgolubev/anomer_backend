#!/bin/bash

# Создает .env.example на основе существующего .env файла.
# Формат строки в .env файле:
# ```
# # example: "example_value" # какой-то комментарий
# PARAMETER="some secret value"
# ```
#
# Скрипт распарсит комментарий и выполнит подстановку:
# ```
# PARAMETER="example_value" # какой-то комментарий
# ```

# проверка .env
[ -f .env ] || { echo "❌ .env не найден"; exit 1; }

# предыдущая строка
prev=""

# читаем .env
while IFS= read -r line || [ -n "$line" ]; do

  # строка переменной
  if [[ "$line" =~ ^[[:space:]]*[A-Z_][A-Z0-9_]*[[:space:]]*= ]]; then

        # есть комментарий example
        if [[ "$prev" =~ ^[[:space:]]*#.*example:[[:space:]]*(.*) ]]; then
            # берем example
            example="${BASH_REMATCH[1]}"
        else
            # сохраняем предыдущую строку
            [ -n "$prev" ] && echo "$prev" >> .env.example.tmp
            # сброс example
            example=""
        fi

        # значение по умолчанию
        [ -z "$example" ] && example="your_value"

        # имя переменной
        var=$(echo "$line" | sed 's/^[[:space:]]*\([A-Z_][A-Z0-9_]*\).*/\1/')

        # пишем в пример
        echo "${var}=${example}" >> .env.example.tmp

        # очищаем prev
        prev=""
  else
        # сохраняем prev если есть
        [ -n "$prev" ] && echo "$prev" >> .env.example.tmp

        # ставим текущую как prev
        prev="$line"
  fi
done < .env  # конец чтения

# доп. строка
if [ -n "$prev" ] && ! [[ "$prev" =~ ^[[:space:]]*#.*example: ]]; then 
    echo "$prev" >> .env.example.tmp; 
fi

# переименовываем в .env.example
mv .env.example.tmp .env.example
# говорим юзеру все ок
echo "✅ .env.example создано"