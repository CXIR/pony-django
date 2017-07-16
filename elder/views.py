from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'user/profile.html', locals())


def contact(request):
    form = ContactOldPerson(request.POST or None)

    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Envoi du msg au destinataire

    return render(request, 'user/contact.html', locals())


def findoldperson(request):
    return render(request, 'user/find_old_person.html', locals())
