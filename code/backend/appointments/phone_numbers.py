import phonenumbers
from django.conf import settings
from django.utils.translation import gettext as _


class InvalidPhoneNumber(Exception):
    pass


def get_normalized_phone_number(raw_phone_number, check_validity=False):
    try:
        parsed_data = phonenumbers.parse(raw_phone_number, "HU")
    except phonenumbers.NumberParseException:
        raise InvalidPhoneNumber(_('Include "+" sign, country code and area code.'))

    if phonenumbers.is_valid_number(parsed_data):
        return phonenumbers.format_number(parsed_data, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    if check_validity:
        raise InvalidPhoneNumber(_('Include "+" sign, country code and area code.'))
    return raw_phone_number
