#!/usr/bin/env python
"""
Простой скрипт для запуска тестов.
"""
import os
import sys
import subprocess

# Устанавливаем переменную окружения
os.environ['DJANGO_SETTINGS_MODULE'] = 'question_answer_project.settings'

# Запускаем pytest
result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print(result.stderr)

sys.exit(result.returncode)
