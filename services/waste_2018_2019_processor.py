"""
This method will fetch data from the
"""
from common import file_names
from common import values
import services.energy_saved_processor as energy_processor

import pandas as pd


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
        for waste_type in values.TARGET_WASTE_TYPES:

            # Get the target row for current waste type
            target_row = current_year_df[current_year_df["Waste Type"] == waste_type]
            print(f"=========START===={waste_type} IN  {year}")
            print(target_row)
            print(f"=========END===={waste_type} IN  {year}")
            print("\t\t\t\t")
            # Check if row is not empty
            if len(target_row) > 0:
                total_recycled = target_row.iloc[0]["Total Recycled ('000 tonnes)"]
                print(f"\nTotal recycled for {waste_type} is {total_recycled}")

                total_recycled = float(total_recycled)

                # Fetch the conversion factor
                # Conversion factor is the number of KwH that one metric tonne can produce
                conversion_factor = energy_processor.get_conversion_factor(target_row.iloc[0]["Waste Type"])
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
