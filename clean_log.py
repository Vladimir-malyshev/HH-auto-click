import os

log_file = r'd:\VSCODE\Projects\HH-auto-click\applications.log'

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Remove lines with bad encoding (spaced out characters)
    if '2 0 2 6' in line and ' ' in line[line.find('2 0 2 6'):line.find('2 0 2 6')+10]:
        continue
    if line.strip() == '':
        continue
    new_lines.append(line.strip() + '\n')

# Ensure we don't have duplicates of the new entries if the script is run multiple times
# (actually we just want to keep the file clean)

with open(log_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
