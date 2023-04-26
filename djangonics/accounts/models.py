from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    contact_number = models.CharField(max_length=15)
    pass