from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('token/', views.authorization, name='AUTH'),
    path('polls/create/', views.poll_create, name='POLL_CREATING'),
    path('polls/update_or_delete/<int:poll_id>/', views.poll_update_or_delete, name='POLL_UPDATE_OR_DELETE'),
    path('polls/available/', views.polls_for_user, name='POLLS_FOR_USER'),

    path('question/create/', views.question_create, name='QUESTION_CREATE'),
    path('question/update_or_delete/<int:question_id>/', views.question_update_or_delete, name='QUESTION_UPDATE_OR_DELETE'),

    path('choice/create/', views.choice_create, name='CHOICE_CREATE'),
    path('choice/update_or_delete/<int:choice_id>/', views.choice_update_or_delete, name='CHOICE_UPDATE_OR_DELETE'),

    path('answer/create/', views.answer_create, name='ANSWER_CREATE'),
    path('answer/view/<int:user_id>/', views.answers_for_user, name='ANSWERS_FOR_USER'),
]