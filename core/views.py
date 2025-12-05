from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

import git


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo('/home/sidneygyne/clonex')
        origin = repo.remotes.origin

        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def home(request):
    if request.user.is_authenticated:
        # Usuário já logado → só renderiza index sem formulário
        return render(request, "index.html")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")  # redireciona para o feed após login
    else:
        form = AuthenticationForm()

    return render(request, "index.html", {"form": form})


def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")
    else:
        form = AuthenticationForm()

    return render(request, "index.html", {"form": form})