from django.db import models
from django.utils import timezone
import uuid


class Question(models.Model):
    """
    Модель вопроса.
    
    Содержит информацию о вопросе с текстом и временем создания.
    """
    text = models.TextField(
        verbose_name="Текст вопроса",
        help_text="Введите текст вопроса"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        default=timezone.now,
        help_text="Время создания вопроса"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Возвращает строковое представление вопроса."""
        return f"Вопрос #{self.id}: {self.text[:50]}..."


class Answer(models.Model):
    """
    Модель ответа на вопрос.
    
    Содержит информацию об ответе, связь с вопросом и идентификатор пользователя.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос",
        help_text="Вопрос, на который дан ответ"
    )
    user_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="ID пользователя",
        help_text="Уникальный идентификатор пользователя (UUID)"
    )
    text = models.TextField(
        verbose_name="Текст ответа",
        help_text="Введите текст ответа"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        default=timezone.now,
        help_text="Время создания ответа"
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Возвращает строковое представление ответа."""
        return f"Ответ #{self.id} от пользователя {self.user_id} на вопрос #{self.question.id}: {self.text[:50]}..."
