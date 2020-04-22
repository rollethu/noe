import pytest

from appointments import phone_numbers


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("06201231234", "+36 20 123 1234"),
        ("0620123", "0620123"),
        ("0611231234", "+36 1 123 1234"),
        ("06701231234", "+36 70 123 1234"),
        ("+36701231234", "+36 70 123 1234"),
        ("+3611231234", "+36 1 123 1234"),
        ("+442083661177", "+44 20 8366 1177"),
    ],
)
def test_phone_number_parsing(input_data, expected):
    assert phone_numbers.get_normalized_phone_number(input_data) == expected
