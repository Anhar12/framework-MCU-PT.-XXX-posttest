from django.core.management.base import BaseCommand
from faker import Faker
from MCU.models import Users, Regis, Result
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users', type=int, default=15, help='Number of users to create'
        )
        parser.add_argument(
            '--doctors', type=int, default=5, help='Number of doctors to create'
        )
        parser.add_argument(
            '--regis', type=int, default=20, help='Number of regis to create'
        )
        parser.add_argument(
            '--results', type=int, default=20, help='Number of results to create'
        )

    def handle(self, *args, **options):
        fake = Faker('id_ID') 

        num_users = options['users']
        num_doctors = options['doctors']
        num_regis = options['regis']
        num_results = options['results']

        users = []
        doctors = []
        
        for _ in range(num_users):
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()
            
            user = Users.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=Users.USER
            )
            
            users.append(user)
        
        for _ in range(num_doctors):
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()
            
            doctor = Users.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=Users.DOCTOR
            )
            
            doctors.append(doctor)

        regis = []
        for _ in range(num_regis):
            user = random.choice(users)
            date = fake.date_between(start_date='today', end_date='+1y')

            regis_entry = Regis.objects.create(
                id_user=user,
                date=date
            )
            regis.append(regis_entry)
            
        
        for _ in range(num_results):
            available_regis = [entry for entry in regis if not entry.is_done]
            if not available_regis:
                break
            
            regis_entry = random.choice(available_regis)
            doctor = random.choice(doctors)  
            result = random.choice([Result.P1, Result.P2, Result.P3, Result.P4, Result.P5, Result.P6, Result.P7])
            notes = fake.text()
            start_date = regis_entry.date
            date = fake.date_between(start_date=start_date, end_date='+1y')

            Result.objects.create(
                id_mcu_regis=regis_entry,
                id_doctor=doctor,
                result=result,
                notes=notes,
                date=date
            )

            regis_entry.is_done = True
            regis_entry.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {num_users} users, {num_regis} regis, and {num_results} results. Regis marked as done when Result created.'
        ))
