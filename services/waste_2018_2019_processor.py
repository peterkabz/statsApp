"""
This method will fetch data from the
"""
from classes.file_column_processor import get_waste_type_labels
from common import file_names
from common import values
import services.energy_saved_processor as energy_processor

import pandas as pd

from classes.waste_type import WasteType


def get_energy_saved():
    df = pd.read_csv(file_names.GENERATED_BY_TYPE)

    '''
    Get the relevant row within the target years
    '''
    df = df[(df['Year'] >= values.MIN_TARGET_YEAR) & (df['Year'] <= values.MAX_TARGET_YEAR)]
    result = {}

    '''For each year DO:
         Sum up all the energy saved for each waste type and set it as the year's total
         
      Add the year to the results dict   
    '''

    for year in range(values.MIN_TARGET_YEAR, values.MAX_TARGET_YEAR + 1):

        # Get all records for the current year
        current_year_df = df[df["Year"] == year]

        # Initialize the current year total
        year_total = 0

        '''
            For each waste type
        '''

        for enum_name, waste_type_enum in WasteType.__members__.items():
            waste_type_labels = get_waste_type_labels(enum_name)
            print(f"Waste Type Enum = {waste_type_enum}: ==> {waste_type_labels}")

            # Get the target row for current waste type
            target_rows = current_year_df[current_year_df["Waste Type"].isin(waste_type_labels)]
            print(f"=========START===={waste_type_labels} IN  {year}")
            print(target_rows)
            print(f"=========END===={waste_type_labels} IN  {year}")
            print("\t\t\t\t")
            # Check if row is not empty
            if len(target_rows) > 0:

                # This data in stored in thousand tonnes, so we need to convert to tonnes
                total_thousands_recycled = target_rows["Total Recycled ('000 tonnes)"].sum()
                total_recycled = total_thousands_recycled * 1000

                print(f"\nTotal recycled for {waste_type_labels} is {total_recycled}")

                total_recycled = float(total_recycled)

                # Fetch the conversion factor
                # Conversion factor is the number of KwH that one metric tonne can produce
                conversion_factor = energy_processor.get_conversion_factor(enum_name)
                conversion_factor = float(conversion_factor)

                # Calculate the energy saved for the current waste type in the current year
                # Using the conversion factor
                energy_saved = \
                    total_recycled * conversion_factor

                year_total += energy_saved
                print(energy_saved)

        result[year] = year_total

        print(result.items())
    return result

