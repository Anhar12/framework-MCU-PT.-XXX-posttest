from django.db import models
from django.utils import timezone
from . import Users
from . import Regis
import re

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
    
    def save(self, *args, **kwargs):
        if not self.no_document:
            day = self.date.day
            month = self.date.strftime("%m")
            year = self.date.strftime("%y")
            
            roman_months = {
                '01': 'I',
                '02': 'II',
                '03': 'III',
                '04': 'IV',
                '05': 'V',
                '06': 'VI',
                '07': 'VII',
                '08': 'VIII',
                '09': 'IX',
                '10': 'X',
                '11': 'XI',
                '12': 'XII',
            }
            roman_month = roman_months[month]

            existing_documents = Result.objects.filter(date=self.date)

            if existing_documents.exists():
                max_antrean = 0
                for doc in existing_documents:
                    match = re.search(r'/(\d+)$', doc.no_document)
                    if match:
                        antrean = int(match.group(1))
                        if antrean > max_antrean:
                            max_antrean = antrean

                next_antrean = max_antrean + 1
            else:
                next_antrean = 1

            self.no_document = f"XXX/MCU/{day:02}/{roman_month}/{year}/{next_antrean}"
            
        self.id_mcu_regis.is_done = True
        self.id_mcu_regis.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Result for {self.id_mcu_regis.id_user.username} - Doctor: {self.id_doctor.username} - Document: {self.no_document}"
