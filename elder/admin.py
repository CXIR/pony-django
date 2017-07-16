from django.contrib import admin
from elder.models import *

# Register your models here.
admin.site.register(OldPerson)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(OldPersonAnswers)
admin.site.register(History)