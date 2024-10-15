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
        if self._state.adding:
            max_no_antrean = Regis.objects.filter(date=self.date).aggregate(models.Max('no_antrean'))['no_antrean__max']
            self.no_antrean = max_no_antrean + 1 if max_no_antrean else 1
        else:
            old_instance = Regis.objects.get(pk=self.pk)
            if old_instance.date != self.date:
                max_no_antrean = Regis.objects.filter(date=self.date).aggregate(models.Max('no_antrean'))['no_antrean__max']
                self.no_antrean = max_no_antrean + 1 if max_no_antrean else 1
                self.update_no_antrean_after_delete(old_instance.date, old_instance.no_antrean)

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        deleted_date = self.date
        deleted_no_antrean = self.no_antrean
        super().delete(*args, **kwargs)
        self.update_no_antrean_after_delete(deleted_date, deleted_no_antrean)
        
    def update_no_antrean_after_delete(self, date, deleted_no_antrean):
        regis_to_update = Regis.objects.filter(date=date, no_antrean__gt=deleted_no_antrean).order_by('no_antrean')
        for regis in regis_to_update:
            regis.no_antrean -= 1
            regis.save()

    def __str__(self):
        return f"Antrean {self.no_antrean} - {self.id_user.first_name} {self.id_user.last_name} - {self.date}"
