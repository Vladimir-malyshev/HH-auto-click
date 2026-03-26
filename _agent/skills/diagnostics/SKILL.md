# НАВЫК: diagnostics

## Название
`diagnostics`

## Описание
Диагностика окружения: проверяет доступные инструменты субагента и структуру файлов проекта.
Запускать при любых непонятных ошибках или после изменений в проекте.

## Команды
- `run_diagnostics()`: Запускает полную диагностику.

## Детали реализации

### Шаг 1 — Проверка доступных инструментов

Попытаться вызвать каждый из перечисленных инструментов с минимальными безопасными параметрами.
Записать результат: `OK` или `ОШИБКА: [текст]`.

Список инструментов для проверки:
- `read_file("cover_letters/ai_leader.txt")` — чтение файла
- `write_file("diagnostics_test.tmp", "test")` — запись файла
- `list_directory(".")` — список файлов в корне проекта
- `execute_browser_javascript("return 1+1")` — выполнение JS в браузере
- `browser_navigate("about:blank")` — навигация браузера

После проверки удалить `diagnostics_test.tmp` если он был создан.

### Шаг 2 — Проверка структуры файлов

Выполнить `list_directory(".")` и `list_directory("cover_letters")`.

Убедиться что существуют:
- `cover_letters/ai_leader.txt` — ОБЯЗАТЕЛЬНО
- `cover_letters/ai_product_manager.txt` — ОБЯЗАТЕЛЬНО
- `applications.log` — создать если отсутствует (пустой файл)
- `_agent/skills/hh_apply/SKILL.md` — ОБЯЗАТЕЛЬНО

### Шаг 3 — Проверка содержимого писем

Прочитать оба файла:
- `cover_letters/ai_leader.txt`
- `cover_letters/ai_product_manager.txt`

Для каждого проверить:
- Файл не пустой
- Длина > 100 символов
- Не содержит слов: test, hello, asdf, проверка, TODO, placeholder

### Шаг 4 — Отчёт

Вывести итог в формате:

```
=== ДИАГНОСТИКА [дата время] ===

ИНСТРУМЕНТЫ:
- read_file: OK / ОШИБКА
- write_file: OK / ОШИБКА
- list_directory: OK / ОШИБКА
- execute_browser_javascript: OK / ОШИБКА
- browser_navigate: OK / ОШИБКА

ФАЙЛЫ:
- ai_leader.txt: OK ([N] символов) / НЕ НАЙДЕН
- ai_product_manager.txt: OK ([N] символов) / НЕ НАЙДЕН
- applications.log: OK / СОЗДАН / ОШИБКА
- SKILL.md: OK / НЕ НАЙДЕН

ИТОГ: ГОТОВ К РАБОТЕ / ЕСТЬ ПРОБЛЕМЫ (список)
================================
```

Записать отчёт в `applications.log` ОБЯЗАТЕЛЬНО!!!!
