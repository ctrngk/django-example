from django.shortcuts import render

# Create your views here.
########################################
# login/views.py
########################################


from login.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/account/register/success/')
    else:
        form = RegistrationForm()

    variables = {
        'form': form
    }
    return render(
        request,
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render(
        request,
        'registration/success.html',
    )





