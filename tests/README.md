# 🧪 Тесты API эндпоинтов AskMe

## Структура тестов

```
tests/
├── __init__.py              # Пакет тестов
├── conftest.py              # Конфигурация pytest и фикстуры
├── test_views.py            # Тесты API эндпоинтов
└── README.md                # Документация тестов
```

## Тестируемые эндпоинты

### Вопросы (Questions)
- ✅ `GET /api/questions/` - список всех вопросов
- ✅ `POST /api/questions/` - создание нового вопроса
- ✅ `GET /api/questions/{id}/` - получение вопроса с ответами
- ✅ `DELETE /api/questions/{id}/` - удаление вопроса

### Ответы (Answers)
- ✅ `POST /api/questions/{id}/answers/` - добавление ответа к вопросу
- ✅ `GET /api/answers/{id}/` - получение конкретного ответа
- ✅ `DELETE /api/answers/{id}/` - удаление ответа

## Запуск тестов

### Быстрый запуск

**Windows:**
```cmd
run_tests.bat
```

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Ручной запуск

```bash
# Активация виртуального окружения
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements-test.txt

# Запуск всех тестов
python -m pytest tests/ -v

# Запуск с покрытием кода
python -m pytest tests/ --cov=askme --cov-report=html

# Запуск конкретного класса тестов
python -m pytest tests/test_views.py::TestQuestionsAPI -v

# Запуск конкретного теста
python -m pytest tests/test_views.py::TestQuestionsAPI::test_get_questions_list_empty -v

# Запуск с фильтром
python -m pytest tests/ -k "test_question" -v
```

## Полезные команды

### Просмотр покрытия кода
```bash
# Генерация HTML отчета
python -m pytest tests/ --cov=askme --cov-report=html

# Открыть отчет в браузере
# Windows: start htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
# Mac: open htmlcov/index.html
```

### Отладка тестов
```bash
# Подробный вывод
python -m pytest tests/ -v

# Остановка на первой ошибке
python -m pytest tests/ -x

# Запуск только упавших тестов
python -m pytest tests/ --lf

# Запуск с отладочной информацией
python -m pytest tests/ -s
```

### Фильтрация тестов
```bash
# По маркерам
python -m pytest tests/ -m "not slow"

# По паттерну имени
python -m pytest tests/ -k "test_question"

# По классу
python -m pytest tests/test_models.py::TestQuestionModel
```

## Фикстуры

### Основные фикстуры (`conftest.py`)

- `api_client` - APIClient для тестирования API
- `sample_question` - тестовый вопрос
- `sample_questions` - несколько тестовых вопросов
- `sample_answer` - тестовый ответ
- `sample_answers` - несколько тестовых ответов
- `question_data` - данные для создания вопроса
- `answer_data` - данные для создания ответа
- `invalid_question_data` - невалидные данные вопроса
- `invalid_answer_data` - невалидные данные ответа

### Использование фикстур

```python
def test_example(api_client, sample_question):
    """Пример использования фикстур."""
    url = reverse('question-detail', kwargs={'pk': sample_question.id})
    response = api_client.get(url)
    assert response.status_code == 200
```

## Маркеры тестов

```python
@pytest.mark.slow
def test_slow_operation():
    """Тест медленной операции."""
    pass

@pytest.mark.integration
def test_api_integration():
    """Интеграционный тест API."""
    pass
```

## Настройка pytest

Конфигурация в `pytest.ini`:
- Автоматическое обнаружение тестов
- Настройка Django
- Маркеры тестов
- Опции по умолчанию

## Добавление новых тестов

### 1. Создание нового тестового файла

```python
# tests/test_new_feature.py
import pytest
from django.urls import reverse

class TestNewFeature:
    def test_new_functionality(self, api_client):
        """Тест новой функциональности."""
        # Ваш тест здесь
        pass
```

### 2. Добавление теста в существующий файл

```python
def test_new_test_case(self, api_client, sample_question):
    """Новый тест-кейс."""
    # Ваш тест здесь
    pass
```

### 3. Создание новой фикстуры

```python
# В conftest.py
@pytest.fixture
def new_fixture():
    """Новая фикстура."""
    return "test_data"
```

## Лучшие практики

1. **Именование тестов** - используйте описательные имена
2. **Один тест - одна проверка** - каждый тест должен проверять одну вещь
3. **Используйте фикстуры** - для переиспользования тестовых данных
4. **Тестируйте граничные случаи** - пустые данные, невалидные данные
5. **Покрытие кода** - стремитесь к высокому покрытию
6. **Быстрые тесты** - избегайте медленных операций в unit тестах

## Troubleshooting

### Проблемы с базой данных
```bash
# Очистка тестовой базы данных
python manage.py flush --noinput

# Применение миграций
python manage.py migrate
```

### Проблемы с зависимостями
```bash
# Переустановка зависимостей
pip install -r requirements-test.txt --force-reinstall
```

### Проблемы с импортами
```bash
# Проверка PYTHONPATH
python -c "import sys; print(sys.path)"

# Запуск из корневой директории проекта
cd /path/to/project
python -m pytest tests/
```
