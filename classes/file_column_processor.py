import os

from classes.waste_type import WasteType


def get_waste_type_labels(waste_type_enum):
    string_labels = os.getenv(waste_type_enum)
    return string_labels.split(",") if string_labels is not None else []
