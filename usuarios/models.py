from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(User):
    telefono= models.BigIntegerField()

    def __str__(self):
        return self.get_full_name()