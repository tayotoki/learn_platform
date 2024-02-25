import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Загрузка данных в базу данных из SQL-скрипта'

    def handle(self, *args, **options):
        script_path = settings.BASE_DIR / "db_dump.sql"

        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        command = [
            'psql',
            '-U', db_user,
            '-d', db_name,
            '-h', db_host,
            '-p', db_port,
            '-f', script_path
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            errors = result.stderr
            output = result.stdout

            if errors:
                self.stdout.write(self.style.ERROR(errors))
                self.stdout.write(self.style.ERROR('Произошла ошибка при выполнении команды.'))
            else:
                self.stdout.write(self.style.SUCCESS(output))
                self.stdout.write(self.style.SUCCESS('Данные успешно загружены в базу данных.'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(e.stderr))
            self.stdout.write(self.style.ERROR('Произошла ошибка при выполнении команды.'))
