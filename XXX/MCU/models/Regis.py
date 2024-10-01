from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from . import Users

class Regis(models.Model):
    id_user = models.ForeignKey(Users, limit_choices_to={'role': Users.USER, 'is_superuser': False},on_delete=models.CASCADE)
    no_antrean = models.IntegerField(editable=False)
    date = models.DateField(default=timezone.now)
    is_done = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.no_antrean is None:
            max_no_antrean = Regis.objects.filter(date=self.date).aggregate(models.Max('no_antrean'))['no_antrean__max']
            self.no_antrean = max_no_antrean + 1 if max_no_antrean else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Antrean {self.no_antrean} - {self.id_user.username} - {self.date}"
