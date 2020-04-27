import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from cryptography.fernet import Fernet
from appointments.models import Location, TimeSlot


class Command(BaseCommand):
    help = "Create timeslots for the ONLY location currently available"

    def add_arguments(self, parser):
        parser.add_argument("start", type=dt.datetime.fromisoformat)
        parser.add_argument("end", type=dt.datetime.fromisoformat)
        parser.add_argument("duration", type=int)
        parser.add_argument("capacity", type=int)

    def handle(self, *args, **options):
        self.stdout.write(str(type(options["start"])) + str(options["start"]))
        start = timezone.make_aware(options["start"])
        end = timezone.make_aware(options["end"])
        duration = dt.timedelta(minutes=options["duration"])
        location = Location.objects.get()

        self.stdout.write(f"Creating TimeSlots with start={start} end={end}")
        time_slots = TimeSlot.objects.create_time_slots(
            locations=[location], start=start, end=end, duration=duration, capacity=options["capacity"]
        )

        self.stdout.write(f"Created {len(time_slots)} TimeSlots:")
        for time_slot in time_slots:
            self.stdout.write(f"{time_slot.start} - {time_slot.end}")
        self.stdout.write("Done.")
