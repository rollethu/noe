class PaymentException(Exception):
    pass


class InvalidSignature(PaymentException):
    pass
