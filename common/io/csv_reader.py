import csv


class CsvReader:
    @staticmethod
    def read_csv_to_dict(source_file):
        with open(source_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)
            if len(rows) > 0:
                print(f"Non empty data read from {source_file}")
            return csv_reader
