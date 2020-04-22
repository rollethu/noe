import pytest

from appointments import licence_plates


@pytest.mark.parametrize(
    "input_data, expected", [("a", "A"), ("A", "A"), ("á", "A"), ("abc-123", "ABC123"), ('$abc "-& 1 2  3', "ABC123")]
)
def test_licence_plate_normalization(input_data, expected):
    assert licence_plates.get_normalized_licence_plate(input_data) == expected
