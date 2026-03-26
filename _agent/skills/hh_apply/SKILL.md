# НАВЫК: hh_apply

## Название
`hh_apply`

## Описание
Автоматизирует отклики на вакансии на `hh.ru`. Содержит всю техническую реализацию процесса.

## Команды
- `apply_to_search(search_url)` — запустить отклики для страницы поиска.
- `run_diagnostics()` — проверить окружение перед работой.

## Диагностика (run_diagnostics)

Выполнить перед первым запуском или при любой ошибке.

1. Проверить каждый инструмент минимальным вызовом:
   - `read_file("cover_letters/ai_leader.txt")`
   - `write_file("diagnostics_test.tmp", "test")` → затем удалить файл
   - `list_directory(".")`
   - `execute_browser_javascript("return 1+1")`
   - `browser_navigate("about:blank")`

2. Проверить файлы:
   - `cover_letters/ai_leader.txt` — обязателен, длина > 100 символов
   - `cover_letters/ai_product_manager.txt` — обязателен, длина > 100 символов
   - `applications.log` — создать если отсутствует

3. Записать отчёт в `applications.log` **обязательно**:
```
=== ДИАГНОСТИКА [дата время] ===
ИНСТРУМЕНТЫ:
- read_file: OK / ОШИБКА
- write_file: OK / ОШИБКА
- list_directory: OK / ОШИБКА
- execute_browser_javascript: OK / ОШИБКА
- browser_navigate: OK / ОШИБКА
ФАЙЛЫ:
- ai_leader.txt: OK ([N] симв.) / НЕ НАЙДЕН
- ai_product_manager.txt: OK ([N] симв.) / НЕ НАЙДЕН
- applications.log: OK / СОЗДАН
ИТОГ: ГОТОВ К РАБОТЕ / ЕСТЬ ПРОБЛЕМЫ: [список]
================================
```

## Основной процесс (apply_to_search)

Для **каждой** вакансии на странице:

### Шаг 1 — Проверка статуса
Если у вакансии статус "Вы откликнулись" — пропустить, перейти к следующей.

### Шаг 2 — Открыть форму отклика
Нажать "Откликнуться" прямо в списке, без перехода на страницу вакансии.

### Шаг 3 — Выбор резюме
- Название содержит Product, Manager, Owner, Владелец, Менеджер → "AI Product Manager"
- Иначе → "AI Product Leader"

### Шаг 4 — Поле ожидаемой зарплаты

Проверить наличие поля зарплаты в форме отклика (input с подписью "зарплата" / "ожидаемая зарплата").

Если поле есть — вставить `400000` через `execute_browser_javascript`:
```javascript
(function(value) {
  const input = document.querySelector('input[data-qa="salary-input"]') ||
                document.querySelector('input[type="number"]');
  if (!input) return 'NOT_FOUND';
  const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
  ).set;
  nativeSetter.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
  return input.value;
})('400000')
```
Если вернулось `'NOT_FOUND'` — поля нет, продолжить.

### Шаг 6 — Сопроводительное письмо

**Проверить:** есть ли под полем текст "Обязательное поле для этой вакансии".

**Если НЕ обязательно** — перейти к шагу 5.

**Если обязательно:**

а) Определить файл:
   - PM-роль → `cover_letters/ai_product_manager.txt`
   - Иначе → `cover_letters/ai_leader.txt`

б) Прочитать через `read_file`, сохранить в COVER_TEXT.

в) Валидация COVER_TEXT:
   - Не пустой
   - Длина > 100 символов
   - Не содержит: test, hello, asdf, проверка, TODO, placeholder
   
   Если не прошёл → записать ошибку в лог, перейти к следующей вакансии.

г) Вставить текст через `execute_browser_javascript`:
```javascript
(function(text) {
  const tx = document.querySelector(
    'textarea[data-qa="vacancy-response-letter-informer"]'
  );
  if (!tx) return 'NOT_FOUND';
  const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, 'value'
  ).set;
  nativeSetter.call(tx, text);
  tx.dispatchEvent(new Event('input', { bubbles: true }));
  tx.dispatchEvent(new Event('change', { bubbles: true }));
  return tx.value.length;
})(COVER_TEXT)
```
⚠️ COVER_TEXT подставлять как JS-строку: кавычки экранировать `\"`, переносы строк → `\n`.

д) Проверить результат:
   - Вернулось число > 100 и счётчик в поле не "0из10000" → OK
   - Вернулось `0` или `'NOT_FOUND'` → записать ошибку в лог, перейти к следующей вакансии.

### Шаг 7 — Отправка
Нажать "Откликнуться". Подтвердить успех (кнопка изменилась или появилось сообщение).

### Шаг 8 — Уборка и логирование
- Закрыть все вкладки кроме страницы поиска.
- Записать результат в `applications.log` **обязательно**:
  - Успех: `[Дата время] | [Вакансия] | Резюме: [название] | Письмо: Да/Нет | Статус: Успех`
  - Ошибка: `[Дата время] | ОШИБКА | Инструмент: [имя] | Причина: [текст] | Вакансия: [название]`

### Шаг 9 — Следующая вакансия
Если вакансии на странице закончились — нажать следующую страницу (`a[data-qa="pager-next"]`).
Если страницы кончились — завершить, вывести итоговую статистику из лога.

## КРИТИЧЕСКИЙ ЗАПРЕТ
- ЗАПРЕЩЕНО вставлять текст через `browser_press_key`, `type` или буфер обмена.
- ЗАПРЕЩЕНО использовать `javascript:` в адресной строке браузера.
- ЗАПРЕЩЕНО нажимать "Откликнуться" если счётчик показывает "0из10000".
- ЗАПРЕЩЕНО импровизировать альтернативные способы если что-то не работает — записать ошибку и идти дальше.

## Анти-детект
Рандомизировать задержки 2–5 сек между действиями. Имитировать естественную прокрутку.
