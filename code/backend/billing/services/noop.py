from .interface import BillingService


class NoopService(BillingService):
    """
    Provides no billing service. Does nothing when sending an invoice.
    """

    def send_seat_invoice(self, seat):
        pass

    def send_appointment_invoice(self, appointment):
        pass
