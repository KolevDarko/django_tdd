from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def persona_login(request):
    if request.method == 'POST':
        user = authenticate(assertion=request.POST['assertion'])
        if user:
            login(request, user)
    return HttpResponse('OK')
