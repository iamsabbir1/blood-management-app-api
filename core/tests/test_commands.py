"""
Test custom django management command.
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase, TestCase
from django.conf import settings
import psycopg2
import time


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test Waiting for database if ready"""
        patched_check.return_value = True
        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for databasse when getting OperationalError."""
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])


# class MigrateWithDbTestCase(TestCase):
#     """Test Migrate with Db"""

#     def test_migrate_with_db(self):
#         """Test migrate with db"""
#         db_name = settings.DATABASES["default"]["NAME"]
#         db_user = settings.DATABASES["default"]["USER"]
#         db_password = settings.DATABASES["default"]["PASSWORD"]
#         db_host = settings.DATABASES["default"]["HOST"]
#         db_port = settings.DATABASES["default"]["PORT"]

#         try:
#             # Step 1: Connect to the "postgres" database
#             conn = psycopg2.connect(
#                 dbname="postgres",
#                 user=db_user,
#                 password=db_password,
#                 host=db_host,
#                 port=db_port,
#             )
#             conn.autocommit = True
#             cursor = conn.cursor()

#             # Step 2: Terminate active connections to the target database
#             cursor.execute(
#                 f"""
#                 SELECT pg_terminate_backend(pg_stat_activity.pid)
#                 FROM pg_stat_activity
#                 WHERE pg_stat_activity.datname = '{db_name}'
#                   AND pid <> pg_backend_pid();
#                 """
#             )
#             time.sleep(2)  # Ensure connections are terminated

#             # Step 3: Drop the database if it exists
#             cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
#             if cursor.fetchone():
#                 cursor.execute(f"DROP DATABASE {db_name}")
#                 time.sleep(2)  # Ensure the database is dropped

#             # Step 4: Close connection to "postgres"
#             cursor.close()
#             conn.close()

#         except Exception as e:
#             self.fail(f"Error during database setup: {e}")

#         # Step 5: Run the migrate_with_db command
#         try:
#             call_command("migrate_with_db")
#         except Exception as e:
#             self.fail(f"Error running migrate_with_db: {e}")

#         # Step 6: Verify the database was created successfully
#         try:
#             conn = psycopg2.connect(
#                 dbname="postgres",
#                 user=db_user,
#                 password=db_password,
#                 host=db_host,
#                 port=db_port,
#             )
#             cursor = conn.cursor()
#             cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
#             self.assertIsNotNone(cursor.fetchone(), "Database was not created")
#         finally:
#             cursor.close()
#             conn.close()
