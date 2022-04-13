from django import forms
from .models import *
from django.forms import ClearableFileInput

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class UploadFolderForm(forms.ModelForm):
    class Meta:
        model = UploadFolder
        fields = ['files']
        widgets = {
            'files': ClearableFileInput(attrs={'multiple': True}),
        }