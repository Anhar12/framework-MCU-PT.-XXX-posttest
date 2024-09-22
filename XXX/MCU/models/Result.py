from django.db import models
from django.utils import timezone
from . import Users
from . import Regis

class Result(models.Model):
    NORMAL = 'Normal'
    ABNORMAL = 'Abnormal'

    RESULT_CHOICES = (
        (NORMAL, 'Normal'),
        (ABNORMAL, 'Abnormal'),
    )

    id_mcu_regis = models.ForeignKey(Regis, on_delete=models.CASCADE) 
    id_doctor = models.ForeignKey(Users, limit_choices_to={'role': 1}, on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    no_document = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Result for {self.id_mcu_regis.id_user.username} - Doctor: {self.id_doctor.username}"
