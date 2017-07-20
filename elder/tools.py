from django.contrib.auth.models import User
import smtplib
import re


def send_mail(receivers, message):
    sender = 'mailtest.lud@gmail.com'
    password ='Mailtest2015'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receivers, message)
    server.quit()


def password_verification(password):
    pattern = '^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d$@$!%*#?&]{8,25}$'
    result = re.findall(pattern, password)
    if result:
        return True
    else:
        return False


def username_verification(username):
    user = User.objects.filter(username=username)
    if user is not None:
        return True
    else:
        return False


def delete_accent(str):
    with_accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    without_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']

    for c, s in with_accent, without_accent:
        str = str.replace(c, s)
    return str