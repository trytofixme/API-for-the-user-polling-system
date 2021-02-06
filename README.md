# Описание ТЗ

Задача: спроектировать и разработать API для системы опросов пользователей.
### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

# Инструкция по разворачиванию приложения
### Подготовка проекта к запуску
* Активируем виртуальную среду:
```python
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

* Запускаем проект на django
```python
pip install Django
pip install djangorestframework
django-admin startproject mysite
```
* Перейдем в директорию проекта
```bash
cd mysite
```
* Создаем приложение
```python
django-admin startapp polls
```
* Добавляем надстройки в mysite/settings.py

```python
INSTALLED_APPS = (
    # ... 
    'rest_framework',
    'polls',
)

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'
```
### Запуск проекта
* Синхронизация базы данных с моделями приложений
```python
python3 manage.py makemigrations
python3 manage.py migrate
```
* Создания суперпользователя
```python
python3 manage.py createsuperuser
```

* Запуск сервера
```python
python3 manage.py runserver
```
* Starting development server at http://127.0.0.1:8000/

# Документация API
## Функционал для администратора системы:
### Аутентификация
#### Авторизация в системе
1. URL: http://127.0.0.1:8000/api/v1/token/
2. request : GET
3. Тело ответа :
```json
{
    username, # Строка
    password, # Строка
}
```
### Опросы
#### Добавление опросов
1. URL: http://127.0.0.1:8000/api/v1/polls/create
2. request : POST
3. Тело ответа :
```json
{   
   id, # Натуральное число - id опроса
   poll_name, # Строка
   poll_start_time, # YYYY-MM-DD HH:MM:SS
   poll_finish_time, # YYYY-MM-DD HH:MM:SS
   poll_description # Строка
   questions: [
        {
            id,
            question_text,           
            question_type,       
            choices: [      
                { id, question, choice_text },
                ...
            ]
        },
        ...
    ]
}
```
#### Изменение опросов
1. URL: http://127.0.0.1:8000/api/v1/polls/update_or_delete/<int:poll_id>/
2. request : PATCH
3. Тело ответа :
```json
{
   id, # Натуральное число - id опроса
   poll_name, # Строка
   poll_finish_time, # YYYY-MM-DD HH:MM:SS
   poll_description # Строка
   questions: [
        {
            id,
            question_text,           
            question_type,       
            choices: [      
                { id, question, choice_text },
                ...
            ]
        },
        ...
    ]
}
```

#### Удаление опросов
1. URL: http://127.0.0.1:8000/api/v1/polls/update_or_delete/<int:poll_id>/
2. request : DELETE


### Вопросы в опросах
#### Добавление вопросов в опросе
1. URL: http://127.0.0.1:8000/api/v1/question/create
2. request : POST
3. Тело ответа :
```json
{
   id, # Натуральное число - id вопроса в опросе
   question_text, # Строка
   question_type # Строка
   choices: [      
                { id, question, choice_text },
                ...
            ]
}
```
#### Изменение вопросов в опросе
1. URL: http://127.0.0.1:8000/api/v1/question/update_or_delete/<int:poll_id>/
2. request : PATCH
3. Тело ответа :
```json
{
   id, # Натуральное число - id вопроса в опросе
   question_text, # Строка
   question_type # Строка
   choices: [      
                { id, question, choice_text },
                ...
            ]
}
```

#### Удаление вопросов в опросе
1. URL: http://127.0.0.1:8000/api/v1/question/update_or_delete/<int:poll_id>/
2. request : DELETE

### Варианты выборов в опросе
#### Добавление варианта выбора в опросе
1. URL: http://127.0.0.1:8000/api/v1/choice/create
2. request : POST
3. Тело ответа :
```json
{
   id, # Натуральное число - id варианта выбора в опросе
   question : [
        {id, poll : [...], question_text, question_type, choices : [...]}
   ], 
   choice_text # Строка
}
```
#### Изменение варианта выбора в опросе
1. URL: http://127.0.0.1:8000/api/v1/choice/update_or_delete/<int:choice_id>/
2. request : PATCH
3. Тело ответа :
```json
{
   id, # Натуральное число - id варианта выбора в опросе
   choice_text # Строка
}
```

#### Удаление варианта выбора из опроса
1. URL: http://127.0.0.1:8000/api/v1/choice/update_or_delete/<int:choice_id>/
2. request : DELETE


## Функционал для пользователей системы:
#### Получение списка активных опросов

1. URL: http://127.0.0.1:8000/api/v1/polls/available/
2. request : GET
3. Тело ответа :
```json
[
    {
        poll_name, # Строка
        poll_start_time, # YYYY-MM-DD HH:MM:SS
        poll_finish_time, # YYYY-MM-DD HH:MM:SS
        poll_description # Строка
        questions: [
            {
                id,
                question_text,           
                question_type,       
                choices: [      
                    { id, question, choice_text },
                    ...
                ]
            },
            ...
        ]
    },
    ...
]
```

#### Прохождение опроса
##### Запись ответа
1. URL: http://127.0.0.1:8000/api/v1/answer/create/
2. request : POST
3. Тело ответа :
```json
{
    id, # id ответа
    user_id, # id пользователя
    poll : [{...}]
    question : [{...}]
    choice, # Строка
    choice_text # Строка
}
```
##### Вывод ответа 
1. URL: http://127.0.0.1:8000/api/v1/answer/view/<int:user_id>/
2. request : GET
3. Тело ответа :
```json
[
    {   
        id, # id ответа
        user_id, # id пользователя
        poll : [{...}]
        question : [{...}]
        choice, # Строка
        choice_text # Строка
    },
    ...
]
```
