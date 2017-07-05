import uuid

from django.db import models


class OldPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lasttname = models.CharField(max_length=50)
    birthdate = models.DateField
    login = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    mail = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    weight = models.IntegerField(max_length=3)
    height = models.IntegerField(max_length=3)

    SO_CHOICES = (
        (MEN, 'Men'),
        (WOMEN, 'Women'),
        (BOTH, 'Both'),
    )

    sexualOrientation = models.CharField(max_length=5, choices=SO_CHOICES, default=BOTH)
    ageRangeMin = models.IntegerField(max_length=3)
    ageRangeMax = models.IntegerField(max_length=3)

    def __str__(self):
        return self.id


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField(max_length=100)

    AT_CHOICES = (
        (ONE, 'One answer'),
        (MULTIPLE, 'several answers')
    )

    answerType = models.CharField(max_length=8, choices=AT_CHOICES, default=ONE)

    def __str__(self):
        return self.id


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.TextField(max_length=50)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class OldPersonAnswers(models.Model):
    oldPerson = models.ForeignKey('OldPerson', on_delete=models.CASCADE)
    answers = models.ForeignKey('Answer', on_delete=models.CASCADE)

