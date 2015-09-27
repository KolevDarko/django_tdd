from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import sys

def persona_login(request):
    if request.method == 'POST':
        print("@@@in_post_accounts")
        user = authenticate(assertion=request.POST['assertion'])
        if user:
            login(request, user)
            print("@@@loged the user")
    return HttpResponse('OK')
