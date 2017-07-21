from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.urls import reverse

from elder.forms import ConnexionForm
from elder.models import *
from elder.tools import *


def password_reset(request):
    error = None
    if request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username != '' and email != '' and password1 != '' and password2 != '':
            if password1 == password2:
                if password_verification(password1):
                    user = User.objects.get(username=username)

                    if user is None:
                        error = 'Pseudo incorrect'
                    else:
                        if user.email != email:
                            error = 'Email incorrect'
                        else:
                            user.set_password(password1)
                            user.save()
                            return render(request, 'registration/password_reset_done.html', locals())
                else:
                    error = 'Mot de passe incorrect'
            else:
                error = 'Mot de passe non identique'
        else:
            error = 'Un ou plusieurs champs incorrect'

    return render(request, 'registration/password_reset_form.html', {'error': error})


def login(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
            else:
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'registration/login.html', {'error': error, 'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse(login))


def profile(request):
    return render(request, 'accounts/profile.html', locals())


def registration(request):
    error = None

    if request.POST:
        username = request.POST.get("username")
        print(username)
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        birthday = request.POST.get("birthday")
        description = request.POST.get("description")
        weight = request.POST.get("weight")
        height = request.POST.get("height")
        sexe = request.POST.get("sexe")
        sexualOrientation = request.POST.get("sexualOrientation")
        ageRangeMin = request.POST.get("ageRangeMin")
        ageRangeMax = request.POST.get("ageRangeMax")

        if username != '' and last_name != '' and first_name != '' and email != '' \
                and password1 != '' and password2 != '' and birthday != '' \
                and description != '' and weight != '' and height != '' and sexe != '' \
                and sexualOrientation != '' and ageRangeMin != '' and ageRangeMax != '':
            if password1 == password2:
                if password_verification(password1):
                    if username_verification(username):
                        if ageRangeMin < ageRangeMax:
                            password = password1

                            user = User.objects.create_user(username, email, password)
                            user.first_name = first_name
                            user.last_name = last_name
                            user.save()

                            op = OldPerson()
                            op.user = user
                            op.save()
                            op.birthday = birthday
                            op.description = description
                            op.weight = weight
                            op.height = height
                            op.sexe = sexe
                            op.sexualOrientation = sexualOrientation
                            op.ageRangeMax = ageRangeMax
                            op.ageRangeMin = ageRangeMin
                            op.save()

                            return redirect(login)
                        else:
                            error = "Erreur de saisie dans la tranche d'age"
                    else:
                        error = 'Pseudo déjà utilisé'
                else:
                    error = 'Mot de passe incorrect'
            else:
                error = 'Mot de passe non identique'
        else:
            error = 'Un ou plusieurs champs incorrect'

    return render(request, 'registration/registration.html', {'error': error})


def otherprofile(request):
    current = OldPerson.objects.get(user=request.user)
    msg = None
    seebutton = False  # True : any match
    seemsg = False  # True : match with positive response

    if request.GET:
        person = OldPerson.objects.filter(user=User.objects.get(username=request.GET.get("username"))).first()
        match = current.getmatchwith(person)
        print(match)
        if match is None:
            seebutton = True
        else:
            if match.response == "OK":
                seemsg = True
            elif match.response == "KO":
                msg = 'Pas de love, pas de message'
            elif match.response == 'NO_RESPONSE':
                msg = 'En attente de love'

        return render(request, 'accounts/otherprofile.html',
                      {'person': person, 'seebutton': seebutton, 'seemsg': seemsg, 'msg': msg})
    else:
        submit_value = request.POST.get("submit")
        if submit_value == 'new_match':
            receiver = OldPerson.objects.filter(user=User.objects.get(username=request.POST.get("receiver"))).first()
            new_match = Matching()
            new_match.oldperson1 = current
            new_match.oldperson2 = receiver
            new_match.save()

            return render(request, 'accounts/new_match_confirm.html', {'receiver': receiver.user.username})
        else:
            receiver = OldPerson.objects.filter(user=User.objects.get(username=request.POST.get("receiver")))
            msg = request.POST.get('msg')
            # TODO: send email
            return render(request, 'accounts/msg_send.html',
                          {'sender': current, 'receiver': receiver.user.username, 'msg': msg})

    return render(request, 'accounts/otherprofile.html', {'msg': msg})


def suggest(request):
    current = OldPerson.objects.get(user=request.user)
    suggest = current.getsuggest()

    return render(request, 'accounts/suggest.html', {'suggest': suggest})


def matching(request):
    person = OldPerson.objects.get(user=request.user)
    matches = person.getpositivematch()
    return render(request, 'accounts/matching.html', locals())


def findoldperson(request):
    msg = None
    persons = None
    if request.POST:
        value = request.POST.get("search")
        persons = User.objects.filter(username__icontains=value)
        if len(persons) == 0:
            msg = 'Rien trouvé ! '

    return render(request, 'accounts/find_old_person.html', {'msg': msg, 'persons': persons})


def proposal(request):
    person = OldPerson.objects.get(user=request.user)
    matches = person.getproposal()
    wait = person.getwaitingmatch()
    m_count = len(matches)
    w_count = len(wait)

    if request.POST:
        response = request.POST.get("response")
        u1 = OldPerson.objects.filter(user=User.objects.get(username=request.POST.get("u1"))).first()
        u2 = OldPerson.objects.filter(user=User.objects.get(username=request.POST.get("u2"))).first()
        match = Matching.objects.filter(oldperson1=u1, oldperson2=u2).first()
        match.response = response
        match.save()
        matches = person.getproposal()
        wait = person.getwaitingmatch()
        m_count = len(matches)
        w_count = len(wait)

    return render(request, 'accounts/proposal.html',
                  {'matches': matches, 'm_count': m_count, 'wait': wait, 'w_count': w_count})


def update(request):
    error = None
    current = OldPerson.objects.get(user=request.user)

    if request.POST:
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        password = None

        if password1 != '' and password2 != '':
            if password1 == password2:
                if password_verification(password1):
                    current.user.set_password(password1)
                    current.user.save()
                    user = authenticate(username=current.user.username, password=password1)
                    auth_login(request, user)
                else:
                    error = 'Le mot de passe de respecte pas les conditions'
            else:
                error = "Mot de passe non identique, il n'a pas été modifié"

        current.user.email = request.POST.get("email") if request.POST.get("email") != '' else current.user.email
        current.description = request.POST.get("description") if request.POST.get(
            "description") else current.description
        current.weight = request.POST.get("weight") if request.POST.get("weight") else current.weight
        current.height = request.POST.get("height") if request.POST.get("height") else current.height
        current.sexualOrientation = request.POST.get("sexualOrientation") if request.POST.get(
            "sexualOrientation") else current.sexualOrientation

        current.ageRangeMin = request.POST.get("ageRangeMin") if request.POST.get(
            "ageRangeMin") else current.ageRangeMin
        current.ageRangeMax = request.POST.get("ageRangeMax") if request.POST.get(
            "ageRangeMax") else current.ageRangeMax
        if current.ageRangeMin > current.ageRangeMax:
            min = current.ageRangeMax
            current.ageRangeMax = current.ageRangeMin
            current.ageRangeMin = min

        current.save()

        if error is not None:
            return render(request, 'accounts/update.html', {'error': error})
        else:
            return render(request, 'accounts/profile.html', locals())

    return render(request, 'accounts/update.html', locals())


def user_contact(request):
    sender = OldPerson.objects.get(user=request.user)
    receiver = OldPerson.objects.filter(user=User.objects.get(username=request.POST.get("receiver"))).first()
    message = delete_accent(request.POST.get("msg"))
    email_receiver = receiver.user.email

    message = """
        Bonjour {},
        
        Une demande de contact a ete effectuer par l'utilisateur suivant : {}
        
        Son message est le suivant : 
        {}
        
        Pour le recontacter, vous pouvez lui adresser un mail a l'adresse mail suivante : {}
        
        Cordialement,
        
        
        L'equipe d'Adopte un ieuv

       """.format(receiver.user.get_full_name(), sender.user.username, message,
                  sender.user.email)

    send_mail(email_receiver, message)

    return render(request, 'accounts/msg_send.html', {'receiver': receiver.user.username})
