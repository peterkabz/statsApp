from common import file_names
from collections import Counter
from collections import OrderedDict

from services import waste_2018_2019_processor
from services import waste_stats_processor
import pandas as pd

results_2018_2019 = waste_2018_2019_processor.get_energy_saved()
results_2015_2018 = waste_stats_processor.get_energy_saved()

# Combine the results
results_2015_2018 = Counter(results_2015_2018)
results_2018_2019 = Counter(results_2018_2019)
final_results = results_2018_2019 + results_2015_2018

# Sort the results
final_results = OrderedDict(sorted(final_results.items()))


# Extract data frame
final_df = pd.DataFrame({
    "Year": final_results.keys(),
    "Energy Saved": final_results.values()
})

print("#######################################")
print("##############START FINAL RESULT#####################")
print(final_df)
print("##############END FINAL RESULT#####################")
print("#######################################")

final_df.to_csv("final_results.csv",index=False)



