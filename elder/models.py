from datetime import date
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class OldPerson(models.Model):
    user = models.OneToOneField(User, default=None)
    birthday = models.DateField(verbose_name="Birthday", default=datetime.datetime(1900, 1, 1))
    description = models.TextField(max_length=5000)
    weight = models.IntegerField(default=50)
    height = models.IntegerField(default=150)

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

    def getage(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def gotmatch(self, username):
        op = OldPerson.objects.filter(user=User.objects.get(username=username)).first()
        match = Matching.objects.filter(oldperson1=self, oldperson2=op).first()
        if match is None:
            return False
        else:
            return True

    def getpositivematch(self):
        matches = Matching.objects.filter((Q(oldperson1=self) | Q(oldperson2=self)) & Q(response='OK'))
        return matches

    def getnegativematch(self):
        matches = Matching.objects.filter((Q(oldperson1=self) | Q(oldperson2=self)) & Q(response='KO'))
        return matches

    def getwaitingmatch(self):
        matches = Matching.objects.filter(Q(oldperson1=self) & Q(response='NO_RESPONSE'))
        return matches

    def getproposal(self):
        proposal = Matching.objects.filter(Q(oldperson2=self) & Q(response='NO_RESPONSE'))
        return proposal

    def getallmatch(self):
        matches = Matching.objects.filter((Q(oldperson1=self) | Q(oldperson2=self)))
        return matches

    def getreceivematch(self):
        matches = Matching.objects.filter(oldperson2=self)
        return matches

    def getsendmatch(self):
        matches = Matching.objects.filter(oldperson1=self)
        return matches

    def getmatchwith(self, op):
        match = Matching.objects.filter((Q(oldperson1=self) & Q(oldperson2=op))
                                        | (Q(oldperson1=op) & Q(oldperson2=self))).first()
        return match

    def getsuggest(self):
        r_matches = self.getreceivematch()
        s_matches = self.getsendmatch()
        persons = OldPerson.objects.all().exclude(user=self.user)

        for r in r_matches:
            persons = persons.exclude(user=r.oldperson1.user)

        for s in s_matches:
            persons = persons.exclude(user=s.oldperson2.user)

        return persons


class Matching(models.Model):
    oldperson1 = models.ForeignKey('OldPerson', related_name='oldperson')
    oldperson2 = models.ForeignKey('OldPerson', related_name='oldperson_tomatch')

    R_CHOICES = (
        ('OK', 'Matching'),
        ('KO', 'No Matching'),
        ('NO_RESPONSE', 'No response'),
    )

    response = models.CharField(max_length=15, choices=R_CHOICES, default='NO_RESPONSE')

    def __str__(self):
        str = self.oldperson1.user.username + ' - ' + self.oldperson2.user.username + ' - ' + self.response
        return str
