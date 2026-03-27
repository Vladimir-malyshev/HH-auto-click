import sys

log_file = r'd:\VSCODE\Projects\HH-auto-click\applications.log'

# Read the file and filter out the messed up lines
with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Filter out lines that look like [ 2 0 2 6 ...
new_lines = [line for line in lines if not (line.startswith('[ 2 0 2 6') or line.strip() == '')]

# Add the correct entries
correct_entries = [
    "2026-03-26 19:05 | Руководитель подгруппы (Ozon) | Резюме: AI Product Leader | Письмо: Нет | Статус: Успех\n",
    "2026-03-26 19:05 | Менеджер социальных проектов Райдтеха (Яндекс) | Резюме: AI Product Manager | Письмо: Нет | Статус: Успех\n",
    "2026-03-26 19:05 | Product manager / Продуктовый менеджер по развитию СХД (YADRO) | Резюме: AI Product Manager | Письмо: Нет | Статус: Успех\n",
    "2026-03-26 19:05 | ОШИБКА | Инструмент: hh_apply | Причина: Требуется анкета/доп. вопросы | Вакансия: Business Owner направления SMB (Just AI)\n",
    "2026-03-26 19:05 | ОШИБКА | Инструмент: hh_apply | Причина: Требуется анкета/доп. вопросы | Вакансия: Product Manager (Rsoftware)\n",
    "2026-03-26 19:05 | ОШИБКА | Инструмент: hh_apply | Причина: Требуется анкета/доп. вопросы | Вакансия: E-com Project Manager (product-minded) (85 Тех)\n"
]

with open(log_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    f.write("\n")
    f.writelines(correct_entries)
