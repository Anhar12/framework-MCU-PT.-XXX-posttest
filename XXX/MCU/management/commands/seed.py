from django.core.management.base import BaseCommand
from faker import Faker
from MCU.models import Users, Regis, Result  # Ganti dengan nama app kamu
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users', type=int, default=30, help='Number of users to create'
        )
        parser.add_argument(
            '--regis', type=int, default=15, help='Number of regis to create'
        )
        parser.add_argument(
            '--results', type=int, default=10, help='Number of results to create'
        )

    def handle(self, *args, **options):
        fake = Faker('id_ID') 

        num_users = options['users']
        num_regis = options['regis']
        num_results = options['results']

        users = []
        doctors = []
        user_roles = []  
        for _ in range(num_users):
            email = fake.unique.email()
            username = fake.user_name()
            password = fake.password()
            gender = random.choice([Users.LAKILAKI, Users.PEREMPUAN])
            role = random.choice([Users.USER, Users.DOCTOR])

            user = Users.objects.create(
                email=email,
                username=username,
                password=password,
                gender=gender,
                role=role
            )
            if role == Users.DOCTOR:
                doctors.append(user)
            if role == Users.USER:
                user_roles.append(user)
            users.append(user)

        regis = []
        for _ in range(num_regis):
            user = random.choice(user_roles)  
            no_antrean = random.randint(1, 100)
            date = fake.date_between(start_date='-1y', end_date='today')
            is_done = False  

            regis_entry = Regis.objects.create(
                id_user=user,
                no_antrean=no_antrean,
                date=date,
                is_done=is_done
            )
            regis.append(regis_entry)

        for _ in range(num_results):
            regis_entry = random.choice(regis)
            doctor = random.choice(doctors)  
            result = random.choice([Result.NORMAL, Result.ABNORMAL])
            no_document = fake.unique.bothify(text='DOC####')  
            date = fake.date_between(start_date='-1y', end_date='today')
            notes = fake.text()

            Result.objects.create(
                id_mcu_regis=regis_entry,
                id_doctor=doctor,
                result=result,
                no_document=no_document,
                date=date,
                notes=notes
            )

            regis_entry.is_done = True
            regis_entry.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {num_users} users, {num_regis} regis, and {num_results} results. Regis marked as done when Result created.'
        ))
