import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User


class OldPerson(models.Model):
    user = models.OneToOneField(User, default=None)
    birthdate = models.DateField(auto_now=True)
    description = models.TextField(max_length=5000)
    # avatar = models.ImageField(null=True,blank=True,upload_to="avatars/")
    weight = models.IntegerField(default=150)
    height = models.IntegerField(default=50)

    S_CHOICES = (
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
    )

    sexe = models.CharField(max_length=10, choices=S_CHOICES, default='MEN')

    SO_CHOICES = (
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('BOTH', 'Both'),
    )

    sexualOrientation = models.CharField(max_length=5, choices=SO_CHOICES, default='BOTH')
    ageRangeMin = models.IntegerField(default=50)
    ageRangeMax = models.IntegerField(default=100)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField(max_length=100)

    AT_CHOICES = (
        ('ONE', 'One answer'),
        ('MULTIPLE', 'several answers')
    )

    answerType = models.CharField(max_length=8, choices=AT_CHOICES, default='ONE')

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


class History(models.Model):
    OldPerson = models.ForeignKey('OldPerson', on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
