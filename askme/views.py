from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import Dict, Any

from .models import Question, Answer
from .serializers import (
    QuestionSerializer, 
    QuestionDetailSerializer, 
    AnswerSerializer, 
    AnswerCreateSerializer
)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления вопросами.
    
    Поддерживает операции:
    - GET /questions/ - список всех вопросов
    - POST /questions/ - создать новый вопрос
    - GET /questions/{id}/ - получить вопрос и все ответы на него
    - DELETE /questions/{id}/ - удалить вопрос (вместе с ответами)
    """
    queryset = Question.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Возвращает соответствующий сериализатор в зависимости от действия."""
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer
    
    def list(self, request) -> Response:
        """
        GET /questions/ - получить список всех вопросов.
        
        Returns:
            Response: Список вопросов с количеством ответов
        """
        questions = self.get_queryset()
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
    
    def create(self, request) -> Response:
        """
        POST /questions/ - создать новый вопрос.
        
        Args:
            request: HTTP запрос с данными вопроса
            
        Returns:
            Response: Созданный вопрос или ошибки валидации
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None) -> Response:
        """
        GET /questions/{id}/ - получить вопрос и все ответы на него.
        
        Args:
            request: HTTP запрос
            pk: ID вопроса
            
        Returns:
            Response: Вопрос с ответами или ошибка 404
        """
        try:
            question = get_object_or_404(Question, pk=pk)
            serializer = self.get_serializer(question)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"error": "Вопрос с указанным ID не найден."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None) -> Response:
        """
        DELETE /questions/{id}/ - удалить вопрос (вместе с ответами).
        
        Args:
            request: HTTP запрос
            pk: ID вопроса
            
        Returns:
            Response: Подтверждение удаления или ошибка 404
        """
        try:
            question = get_object_or_404(Question, pk=pk)
            question.delete()  # Каскадное удаление ответов настроено в модели
            return Response(
                {"message": "Вопрос и все его ответы успешно удалены."}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            return Response(
                {"error": "Вопрос с указанным ID не найден."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def answers(self, request, pk=None) -> Response:
        """
        POST /questions/{id}/answers/ - добавить ответ к вопросу.
        
        Args:
            request: HTTP запрос с данными ответа
            pk: ID вопроса
            
        Returns:
            Response: Созданный ответ или ошибки валидации
        """
        try:
            question = get_object_or_404(Question, pk=pk)
            
            serializer = AnswerCreateSerializer(data=request.data)
            if serializer.is_valid():
                answer = serializer.save(question=question)
                response_serializer = AnswerSerializer(answer)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Http404:
            return Response(
                {"error": "Вопрос с указанным ID не найден."}, 
                status=status.HTTP_404_NOT_FOUND
            )


class AnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ответами.
    
    Поддерживает операции:
    - GET /answers/{id}/ - получить конкретный ответ
    - DELETE /answers/{id}/ - удалить ответ
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, pk=None) -> Response:
        """
        GET /answers/{id}/ - получить конкретный ответ.
        
        Args:
            request: HTTP запрос
            pk: ID ответа
            
        Returns:
            Response: Ответ или ошибка 404
        """
        try:
            answer = get_object_or_404(Answer, pk=pk)
            serializer = self.get_serializer(answer)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"error": "Ответ с указанным ID не найден."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None) -> Response:
        """
        DELETE /answers/{id}/ - удалить ответ.
        
        Args:
            request: HTTP запрос
            pk: ID ответа
            
        Returns:
            Response: Подтверждение удаления или ошибка 404
        """
        try:
            answer = get_object_or_404(Answer, pk=pk)
            answer.delete()
            return Response(
                {"message": "Ответ успешно удален."}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            return Response(
                {"error": "Ответ с указанным ID не найден."}, 
                status=status.HTTP_404_NOT_FOUND
            )
