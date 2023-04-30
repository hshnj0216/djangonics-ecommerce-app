import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    contact_number = models.CharField(max_length=15)