from rest_framework import serializers
from .models import Poll, Question, Choice, Answer
from rest_framework import permissions

"""
Структура сериализиторов:
1) Поля
2) С помощью внутреннего класса Meta подкрепляем метаданные модели(связи и т.д.)
3) Если мы хотим иметь возможность возвращать полные экземпляры объектов на основе проверенных данных,
нам нужно реализовать методы .create() и .update()
4) Если нам необходимо проверить экземпляр объекта в процессе создания/изменения/инициализирования сериализитора,
мы должны валидировать получаемые данные.
"""


# Создадим
class UserSerializer:
    def __init__(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=UserSerializer)
    # Используем SlugRelatedField, чтобы презентовать связанные поля ответа с голосованиями, в которых они записаны
    # Как я понял slug_field аналог primary_key, по которому идет связь, поэтому указываем соответствующее поле
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True)
    choice_text = serializers.CharField(max_length=200, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'

    """
    Методы .create() и .update() взяты из документации DRF или можно вот так:
    
    instance.email = validated_data.get('email', instance.email)
    instance.content = validated_data.get('content', instance.content)
    instance.created = validated_data.get('created', instance.created)
    instance.save()
        return instance
    """

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice_text = serializers.CharField(max_length=200)

    class Meta:
        model = Choice
        fields = '__all__'

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question_text = serializers.CharField(max_length=200)
    question_type = serializers.CharField(max_length=200)
    choices = ChoiceSerializer(many=True, read_only=True)

    def validate(self, attrs):
        question_type = attrs['question_type']
        if question_type in ['text', 'one', 'multiple']:
            return attrs
        raise serializers.ValidationError('Invalid question type')

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll_name = serializers.CharField(max_length=200)
    poll_start_time = serializers.DateTimeField()
    poll_finish_time = serializers.DateTimeField()
    poll_description = serializers.CharField(max_length=200)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
