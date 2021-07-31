from common import file_names
from common.io import csv_reader
from services import waste_2018_2019_processor
from services import waste_stats_processor


results = waste_2018_2019_processor.get_energy_saved()
results2 = waste_stats_processor.get_energy_saved()

# TODO combine the results


