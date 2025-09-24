from rest_framework import serializers
from .models import Question, Answer
from typing import Dict, Any


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Question.
    
    Используется для создания и отображения вопросов.
    """
    answers_count = serializers.SerializerMethodField(help_text="Количество ответов на вопрос")
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers_count']
        read_only_fields = ['id', 'created_at', 'answers_count']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].help_text = "Текст вопроса"
        self.fields['created_at'].help_text = "Дата создания вопроса"
    
    def get_answers_count(self, obj: Question) -> int:
        """Возвращает количество ответов на вопрос."""
        return obj.answers.count()


class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения вопроса с ответами.
    """
    answers = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']
        read_only_fields = ['id', 'created_at']
    
    def get_answers(self, obj: Question) -> list[Dict[str, Any]]:
        """Возвращает все ответы на вопрос."""
        answers = obj.answers.all()
        return AnswerSerializer(answers, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Answer.
    
    Используется для создания и отображения ответов.
    """
    question_text = serializers.CharField(source='question.text', read_only=True, help_text="Текст вопроса")
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_text', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'question_text']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].help_text = "ID вопроса"
        self.fields['user_id'].help_text = "UUID пользователя"
        self.fields['text'].help_text = "Текст ответа"
        self.fields['created_at'].help_text = "Дата создания ответа"
    
    def validate_question(self, value: Question) -> Question:
        """
        Валидация существования вопроса.
        
        Args:
            value: Объект вопроса
            
        Returns:
            Question: Валидный объект вопроса
            
        Raises:
            serializers.ValidationError: Если вопрос не существует
        """
        if not Question.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Вопрос с указанным ID не существует.")
        return value


class AnswerCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ответа к конкретному вопросу.
    
    Используется в POST /questions/{id}/answers/
    """
    class Meta:
        model = Answer
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].help_text = "Текст ответа"
    
    def validate_text(self, value: str) -> str:
        """
        Валидация текста ответа.
        
        Args:
            value: Текст ответа
            
        Returns:
            str: Валидный текст
            
        Raises:
            serializers.ValidationError: Если текст пустой
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Текст ответа не может быть пустым.")
        return value.strip()
