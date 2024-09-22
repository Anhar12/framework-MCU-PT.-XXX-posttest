from django.db import models
from django.utils import timezone
from . import Users

class Regis(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    no_antrean = models.IntegerField(default=1)
    date = models.DateField(default=timezone.now)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Antrean {self.no_antrean} - {self.id_user.email}"
