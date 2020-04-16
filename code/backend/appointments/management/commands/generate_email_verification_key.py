from django.core.management.base import BaseCommand, CommandError
from cryptography.fernet import Fernet


class Command(BaseCommand):
    help = (
        "Generate encyption key to email verification. "
        "It needs to be set as EMAIL_VERIFICATION_KEY environment variable."
    )

    def handle(self, *args, **options):
        self.stdout.write("Email verification key: ", ending="")
        self.stdout.write(Fernet.generate_key().decode())
        self.stdout.write("Put this in the EMAIL_VERIFICATION_KEY environment variable!")
