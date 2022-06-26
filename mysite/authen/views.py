from django.shortcuts import render
from .forms import RegisterForm

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()
        return render(response, 'registration/register.html', {'form': form})


