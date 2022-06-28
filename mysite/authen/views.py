from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegisterForm

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/accounts/login')
    else:
        form = RegisterForm()
        return render(response, 'registration/register.html', {'form': form})

# TODO: Fix Registration not working