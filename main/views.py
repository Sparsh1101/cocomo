from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import HttpResponse
import os
from django.conf import settings
# from .logic import processor

@login_required(login_url="main:login")
def index(request):
    if request.method == 'POST':
        form = UploadFolderForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if form.is_valid():
            for f in files:
                file_instance = UploadFolder(files=f)
                file_instance.user = request.user
                file_instance.save()
            # result = processor(request.user.username, time, persons)
            # [loc, cocomo_time, cocomo_persons, time_efficiency, persons_efficiency]
            to_delete = UploadFolder.objects.filter(
                user = request.user
            ).delete()
            os.remove(settings.MEDIA_ROOT + "/" + request.user.username)
            html = "<html><body>Success</body></html>"
            return HttpResponse(html)
        else:
            form = UploadFolderForm()
            return render(request, "index.html", {'form': form})
    else:
        form = UploadFolderForm()
        return render(request, "index.html", {'form': form})


def register(request):
    if request.method == "GET":
        user_creation_form = UserCreationForm()
        return render(
            request, "register.html", context={"user_creation_form": user_creation_form}
        )
    else:
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            Ruser = user_creation_form.save(commit=False)
            Ruser.save()
            return redirect("main:login")
        else:
            return render(
                request,
                "register.html",
                context={"user_creation_form": user_creation_form},
            )


def login(request):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            auth_login(request, user)
            if user is not None:
                return redirect("main:index")
            else:
                message = "User Access Denied!"
                return render(
                    request,
                    "login.html",
                    context={"form": form, "message": message},
                )
        else:
            return redirect("main:index")
    else:
        return render(request, "login.html", context={"form": form, "message": message})


@login_required(login_url="main:login")
def logoutU(request):
    logout(request)
    return redirect("main:login")
