import re
import unidecode


def get_normalized_licence_plate(licence_plate):
    normalized_licence_plate = licence_plate.upper()
    normalized_licence_plate = unidecode.unidecode(normalized_licence_plate)
    normalized_licence_plate = re.sub("[^a-zA-Z0-9]", "", normalized_licence_plate)
    return normalized_licence_plate
