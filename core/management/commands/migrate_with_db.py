import psycopg2
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = "Create database if it does not exist and run migrations"

    def handle(self, *args, **options):
        db_name = settings.DATABASES["default"]["NAME"]
        db_user = settings.DATABASES["default"]["USER"]
        db_password = settings.DATABASES["default"]["PASSWORD"]
        db_host = settings.DATABASES["default"]["HOST"]
        db_port = settings.DATABASES["default"]["PORT"]

        try:
            # Connect to the default database
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Create the database if it doesn't exist
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")
                self.stdout.write(
                    self.style.SUCCESS(f"Database {db_name} created successfully")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Database {db_name} already exists")
                )

            cursor.close()
            conn.close()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating database: {e}"))
            return

        # Run migrations
        call_command("migrate")
