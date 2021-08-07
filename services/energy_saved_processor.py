"""
This method will fetch data about a given waste type from
the energy saved file then calculate the 'conversion factor' used to calculate
the energy saved
"""
from classes.file_column_processor import get_waste_type_labels
from classes.waste_type import WasteType
from common import file_names

import pandas as pd


def get_conversion_factor(waste_type_name):
    waste_type_labels = get_waste_type_labels(waste_type_name)
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
    target = df2[df2["material"].isin(waste_type_labels)]

    factor = 0
    if len(target) > 0:
        print(f"Conversion factor for {waste_type_labels} IS {target.iloc[0]['energy_saved']}")
        factor = target.iloc[0]["energy_saved"]
    return factor



