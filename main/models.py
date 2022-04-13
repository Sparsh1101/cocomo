from django.db import models
from django.contrib.auth.models import User
import os

def rename(instance, filename):
    base, ext = os.path.splitext(filename)
    upload_to = instance.user.username + "/"
    return os.path.join(upload_to, filename)

class UploadFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to=rename)