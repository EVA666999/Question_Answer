from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Question.
    """
    list_display = ('id', 'text_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def text_preview(self, obj: Question) -> str:
        """Возвращает превью текста вопроса."""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Превью текста'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Answer.
    """
    list_display = ('id', 'question', 'user_id', 'text_preview', 'created_at')
    list_filter = ('created_at', 'question')
    search_fields = ('text', 'user_id', 'question__text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def text_preview(self, obj: Answer) -> str:
        """Возвращает превью текста ответа."""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Превью текста'
