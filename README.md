# AskMe API

Простое API для вопросов и ответов на Django REST Framework.

## Описание проекта

AskMe - это REST API для создания вопросов и ответов. Пользователи могут:
- Создавать вопросы
- Добавлять ответы к вопросам
- Просматривать вопросы с ответами
- Удалять вопросы и ответы

## Технологии

- **Django 5.2.6** - веб-фреймворк
- **Django REST Framework** - для создания API
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **pytest** - тестирование

## Быстрый запуск
- 
```bash
pip install -r requirements.txt
```
```bash
docker-compose -f docker-compose.yml up --build
```
```bash
python manage.py runserver
```

### 3. Доступ к API

- **API**: http://localhost:8000/api/
- **Документация**: http://localhost:8000/api/ (Browsable API)

## API Endpoints

### Вопросы
- `GET /api/questions/` - список всех вопросов
- `POST /api/questions/` - создать вопрос
- `GET /api/questions/{id}/` - получить вопрос с ответами
- `DELETE /api/questions/{id}/` - удалить вопрос

### Ответы
- `POST /api/questions/{id}/answers/` - добавить ответ к вопросу
- `GET /api/questions/{id}/answers/` - получить ответы на вопрос
- `GET /api/answers/{id}/` - получить конкретный ответ
- `DELETE /api/answers/{id}/` - удалить ответ

## Тестирование

```bash
pytest -v
```
