from .models import Question, Poll, Choice, Answer
from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer, AnswerSerializer

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, decorators
from rest_framework.response import Response
from django.utils import timezone

"""
Реализовывал views через Function Based Views, а не через Class-based Views, потому что у каждого класса, будут
модификации или сабклассы. То есть структура будет не тривиальной, и ее будет проще разделить на много обособленных
декораторов, которые будет проще менять, вне завиммости от других декораторов.
Да и так как я знаком с django лишь 3 дня, мне проще делать все по гайдам/курсам.


Разделим опрос на методы POST, GET, PATCH, DELETE.
Это делается за тем, чтобы мы не могли обратиться по методу GET к несуществующему опросу.
"""


# добавление опросов.

@decorators.api_view(['POST'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def poll_create(request):
    if request == 'POST':
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# изменение/удаление опросов.

@decorators.api_view(['PATCH', 'DELETE'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def poll_update_or_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'PATCH':
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            survey = serializer.save()
            return Response(PollSerializer(survey).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        poll.delete()
        return Response("{} опрос удален".format(poll_id), status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# добавление вопросов.

@decorators.api_view(['POST'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def question_create(request):
    if request == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# изменение/удаление вопросов.

@decorators.api_view(['PATCH', 'DELETE'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def question_update_or_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("{} вопрос удален".format(question_id), status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Создание вариантов ответа(может только админ)

@decorators.api_view(['POST'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def choice_create(request):
    if request == 'POST':
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Изменение/удаление вариантов ответа(может только админ)
@decorators.api_view(['PATCH', 'DELETE'])
@decorators.permission_classes((IsAuthenticated, IsAdminUser,))
def choice_update_or_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    if request.method == 'PATCH':
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        choice.delete()
        return Response("{} вариант ответа удален".format(choice_id), status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# получение списка активных опросов

@decorators.api_view(['GET'])
@decorators.permission_classes((IsAuthenticated,))
def polls_for_user(request):
    if request == 'GET':
        # Будем использовать timezone.now() вместо datetime.now() из-за удобства формата
        poll = Poll.objects.filter(end_date__gte=timezone.now()).filter(pub_date__lte=timezone.now())
        serializer = PollSerializer(poll, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID,
по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
"""


@decorators.api_view(['POST'])
@decorators.permission_classes((IsAuthenticated,))
def answer_create(request):
    serializer = AnswerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        answer = serializer.save()
        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

@decorators.api_view(['GET'])
@decorators.permission_classes((IsAuthenticated,))
def answers_for_user(request, user_id):
    if request == 'GET':
        answers = Answer.objects.filter(user_id=user_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Подключим авторизацию по токенам
@csrf_exempt
@decorators.api_view(["GET"])
def authorization(request):
    username, password = request.data.get("username"), request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user or username is None or password is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)
