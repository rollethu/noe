from abc import ABC, abstractmethod


class BillingService(ABC):
    """Abstract base class for Billing services."""

    def __init__(self):
        """Should have no parameters.
        It can get it's config values from environment variables, e.g. using os.environ.
        """

    @abstractmethod
    def send_seat_invoice(self, seat):
        ...

    @abstractmethod
    def send_appointment_invoice(self, appointment):
        ...
