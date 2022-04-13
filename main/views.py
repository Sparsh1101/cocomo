from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import HttpResponse
import shutil
from django.conf import settings
# from .logic import processor


@login_required(login_url="main:login")
def index(request):
    timeError = personsError = ""
    if request.method == "POST":
        form = UploadFolderForm(request.POST, request.FILES)
        files = request.FILES.getlist("files")
        time = request.POST["time"]
        persons = request.POST["persons"]
        error = False
        if not request.POST["time"]:
            timeError = "Cannot Be Empty"
            error = True
        elif int(time) <= 0:
            timeError = "Time must be greater than zero"
            error = True

        if not request.POST["persons"]:
            personsError = "Cannot Be Empty"
            error = True   
        elif int(persons) <= 0:
            personsError = "Number of Persons must be greater than zero"
            error = True
        if form.is_valid():
            if error == True:
                return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "show_result": False,
                        "timeError": timeError,
                        "personsError": personsError,
                        "filesError": "",
                        "time": time,
                        "persons": persons,
                    },
                )
            else:
                for f in files:
                    file_instance = UploadFolder(files=f)
                    file_instance.user = request.user
                    file_instance.save()
                # result = processor(request.user.username, time, persons)
                # [loc, cocomo_time, cocomo_persons, time_efficiency, persons_efficiency]
                message = "This is the message"
                result = [1, 2, 3, 4, 5]
                UploadFolder.objects.filter(user=request.user).delete()
                shutil.rmtree(settings.MEDIA_ROOT + "/" + request.user.username)
                return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "result": result,
                        "show_result": True,
                        "timeError": timeError,
                        "personsError": personsError,
                        "message": message,
                        "filesError": "",
                        "time": time,
                        "persons": persons,
                    },
                )
        else:
            return render(
                request,
                "index.html",
                {
                    "form": form,
                    "show_result": False,
                    "timeError": timeError,
                    "personsError": personsError,
                    "filesError": "Cannot be Empty",
                    "time": time,
                    "persons": time,
                },
            )
    else:
        form = UploadFolderForm()
        return render(
            request,
            "index.html",
            {
                "form": form,
                "show_result": False,
                "timeError": timeError,
                "personsError": personsError,
                "filesError": "",
                "time": 0,
                "persons": 0,
            },
        )


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
            if user is not None:
                return redirect("main:index")
            else:
                message = "Username or Password is incorrect"
                return render(
                    request,
                    "login.html",
                    context={"form": form, "message": message},
                )
        else:
            return redirect("main:login")
    else:
        return render(request, "login.html", context={"form": form, "message": message})


@login_required(login_url="main:login")
def logoutU(request):
    logout(request)
    return redirect("main:login")
