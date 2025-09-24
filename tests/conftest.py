"""
Конфигурация pytest для тестов API эндпоинтов.
"""
import pytest
import uuid
from rest_framework.test import APIClient
from askme.models import Question, Answer


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture
def sample_question():
    """Фикстура для создания тестового вопроса."""
    return Question.objects.create(
        text="Как работает Django?"
    )


@pytest.fixture
def sample_answer(sample_question):
    """Фикстура для создания тестового ответа."""
    return Answer.objects.create(
        question=sample_question,
        user_id=uuid.uuid4(),
        text="Django - это веб-фреймворк для Python"
    )
