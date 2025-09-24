"""
Тесты для API эндпоинтов AskMe.
"""
import pytest
import json
import uuid
from django.urls import reverse
from rest_framework import status
from askme.models import Question, Answer


class TestQuestionsAPI:
    """Тесты для эндпоинтов вопросов."""

    @pytest.mark.django_db
    def test_get_questions_list_empty(self, api_client):
        """GET /api/questions/ - пустой список."""
        url = reverse('question-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    @pytest.mark.django_db
    def test_get_questions_list_with_data(self, api_client, sample_question):
        """GET /api/questions/ - список с данными."""
        url = reverse('question-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['text'] == sample_question.text

    @pytest.mark.django_db
    def test_post_questions_create(self, api_client):
        """POST /api/questions/ - создание вопроса."""
        url = reverse('question-list')
        data = {"text": "Как работает Django?"}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert 'id' in response.data

    @pytest.mark.django_db
    def test_post_questions_invalid_data(self, api_client):
        """POST /api/questions/ - невалидные данные."""
        url = reverse('question-list')
        data = {"text": ""}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_get_question_detail(self, api_client, sample_question):
        """GET /api/questions/{id}/ - получение вопроса."""
        url = reverse('question-detail', kwargs={'pk': sample_question.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_question.id
        assert 'answers' in response.data

    @pytest.mark.django_db
    def test_get_question_detail_not_found(self, api_client):
        """GET /api/questions/{id}/ - несуществующий вопрос."""
        url = reverse('question-detail', kwargs={'pk': 999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_question(self, api_client, sample_question):
        """DELETE /api/questions/{id}/ - удаление вопроса."""
        url = reverse('question-detail', kwargs={'pk': sample_question.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Question.objects.filter(id=sample_question.id).exists()

    @pytest.mark.django_db
    def test_delete_question_not_found(self, api_client):
        """DELETE /api/questions/{id}/ - несуществующий вопрос."""
        url = reverse('question-detail', kwargs={'pk': 999})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAnswersAPI:
    """Тесты для эндпоинтов ответов."""

    @pytest.mark.django_db
    def test_get_answer_detail(self, api_client, sample_answer):
        """GET /api/answers/{id}/ - получение ответа."""
        url = reverse('answer-detail', kwargs={'pk': sample_answer.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_answer.id
        assert response.data['text'] == sample_answer.text

    @pytest.mark.django_db
    def test_get_answer_detail_not_found(self, api_client):
        """GET /api/answers/{id}/ - несуществующий ответ."""
        url = reverse('answer-detail', kwargs={'pk': 999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_answer(self, api_client, sample_answer):
        """DELETE /api/answers/{id}/ - удаление ответа."""
        url = reverse('answer-detail', kwargs={'pk': sample_answer.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(id=sample_answer.id).exists()

    @pytest.mark.django_db
    def test_delete_answer_not_found(self, api_client):
        """DELETE /api/answers/{id}/ - несуществующий ответ."""
        url = reverse('answer-detail', kwargs={'pk': 999})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestQuestionAnswersEndpoint:
    """Тесты для эндпоинта добавления ответов к вопросу."""

    @pytest.mark.django_db
    def test_post_question_answers(self, api_client, sample_question):
        """POST /api/questions/{id}/answers/ - добавление ответа."""
        url = reverse('question-answers', kwargs={'pk': sample_question.id})
        data = {"text": "Django - это веб-фреймворк"}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert response.data['question'] == sample_question.id
        assert 'user_id' in response.data

    @pytest.mark.django_db
    def test_post_question_answers_invalid_data(self, api_client, sample_question):
        """POST /api/questions/{id}/answers/ - невалидные данные."""
        url = reverse('question-answers', kwargs={'pk': sample_question.id})
        data = {"text": ""}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_post_question_answers_not_found(self, api_client):
        """POST /api/questions/{id}/answers/ - несуществующий вопрос."""
        url = reverse('question-answers', kwargs={'pk': 999})
        data = {"text": "Ответ"}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_post_question_answers_multiple(self, api_client, sample_question):
        """POST /api/questions/{id}/answers/ - несколько ответов."""
        url = reverse('question-answers', kwargs={'pk': sample_question.id})
        
        # Первый ответ
        response1 = api_client.post(url, data=json.dumps({"text": "Первый ответ"}), content_type='application/json')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Второй ответ
        response2 = api_client.post(url, data=json.dumps({"text": "Второй ответ"}), content_type='application/json')
        assert response2.status_code == status.HTTP_201_CREATED
        
        # Проверяем, что оба ответа созданы
        assert Answer.objects.filter(question=sample_question).count() == 2
