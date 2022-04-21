from platform import processor
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.http import HttpResponse
import shutil
from django.conf import settings
from .logic import processor


def is_admin(user):
    return user.is_superuser


@login_required(login_url="main:login")
def index(request):
    isSuperUser = is_admin(request.user)
    timeError = personsError = modelTypeError = ""
    if request.method == "POST":
        form = UploadFolderForm(request.POST, request.FILES)
        files = request.FILES.getlist("files")
        time = request.POST["time"]
        persons = request.POST["persons"]
        modelType = request.POST["modelType"]
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

        if request.POST["modelType"] == "select":
            modelTypeError = "Please select a valid modelType"
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
                        "modelTypeError": modelTypeError,
                        "personsError": personsError,
                        "filesError": "",
                        "time": time,
                        "persons": persons,
                        "modelType": modelType,
                        "isSuperUser": isSuperUser,
                    },
                )
            else:
                for f in files:
                    file_instance = UploadFolder(files=f)
                    file_instance.user = request.user
                    file_instance.save()

                # result = processor(request.user.username, <software_project_type>, time, persons) # Insert software_project_type input received from user
                # You can print something on these lines for the message part:

                # As per the results of cocomo basic model the time alloted on the project could have been improved by time_efficiency %,
                # the number of person hired for the project could have been improved by efficiency_persons %

                # My recommendation would be to bold the percentages and stuff to make it look good
                # Rest the UI is under you, quite a lot of effort has been put behind the logic
                # please make the UI equally worth it

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
                        "modelTypeError": modelTypeError,
                        "message": message,
                        "filesError": "",
                        "time": time,
                        "persons": persons,
                        "modelType": modelType,
                        "isSuperUser": isSuperUser,
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
                    "modelTypeError": modelTypeError,
                    "filesError": "Cannot be Empty",
                    "time": time,
                    "persons": time,
                    "modelType": modelType,
                    "isSuperUser": isSuperUser,
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
                "modelTypeError": modelTypeError,
                "filesError": "",
                "time": 0,
                "persons": 0,
                "modelType": "select",
                "isSuperUser": isSuperUser,
            },
        )


@user_passes_test(
    lambda user: is_admin(user),
    login_url="main:login",
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
                auth_login(request, user)
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
