"""
This method will fetch data about a given waste type from
the energy saved file then calculate the 'conversion factor' used to calculate
the energy saved
"""
from common import file_names

import pandas as pd

from common.classes.waste_type import WasteType


def get_conversion_factor(waste_type_enum):
    waste_type = get_localized_waste_type(waste_type_enum)
    df = pd.read_csv(file_names.ENERGY_SAVED, skiprows=3, header=None)

    # transpose the columns and row
    transposed = df.transpose()
    # store the transposed data in a file, index=False to avoid numeric indexing on the column names
    # header=None to force automatic header detection
    # TODO: find better way to remove numeric indexing  instead of saving the file
    transposed.to_csv("energy_saved_processed.csv", index=False, header=None)
    df2 = pd.read_csv("energy_saved_processed.csv", na_filter=False)

    # TODO replace missing data

    # remove the Kwh and barrels units on the numbers
    df2['energy_saved'] = df2['energy_saved'].map(lambda x: x.rstrip('KwhWk'))
    df2['crude_oil saved'] = df2['crude_oil saved'].map(lambda x: x.rstrip('barrels'))

    # extract the target row based on the provided argument, waste_type
    target = df2[df2["material"] == waste_type]

    factor = 0
    if len(target) > 0:
        print(f"Conversion factor for {waste_type} IS {target.iloc[0]['energy_saved']}")
        factor = target.iloc[0]["energy_saved"]
    return factor


def get_localized_waste_type(waste_type_enum):
    if waste_type_enum == WasteType.FERROUS_METAL:
        return "Ferrous Metal"
    elif waste_type_enum == WasteType.GLASS:
        return "Glass"
    elif waste_type_enum == WasteType.NON_FERROUS_METAL:
        return "Non-Ferrous Metal"
    elif waste_type_enum == WasteType.PLASTIC:
        return "Plastic"
