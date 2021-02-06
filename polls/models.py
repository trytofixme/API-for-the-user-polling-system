from django.db import models
from django.core.exceptions import ValidationError


class Poll(models.Model):
    poll_name = models.CharField(max_length=100)
    poll_description = models.CharField(max_length=300)
    poll_start_time = models.DateField()
    poll_finish_time = models.DateField()

    def __str__(self):
        return self.poll_name


def check_question_type(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


choice_types = ['CHOICE', 'MULTIPLE_CHOICE']


class Question(models.Model):
    poll_from_question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=30, validators=[check_question_type])
    question_text = models.CharField(max_length=300)

    def __str__(self):
        return self.question_text

    def type(self):
        if self.question_type in choice_types:
            return self.question_type


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.choice_text
