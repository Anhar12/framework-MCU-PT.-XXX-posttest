from django.db import models
from . import Users

class Regis(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Antrean {self.no_antrean} - {self.id_user.email}"
