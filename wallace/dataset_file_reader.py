import csv
import random
import logging

from wallace.dataset import Dataset
from wallace.data_type_classification import DataTypeClassification
from wallace.dataset_cleaner import DatasetCleaner

class DatasetFileReader(object):
    def __init__(self, settings, dataset_filename):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.dataset_filename = dataset_filename

    def read(self, maximum_size=None, delimiter=",", quoting=csv.QUOTE_NONE):
        if maximum_size == None:
            maximum_size = self.settings.get("dataset.maximum_dataset_size")

        with open(self.dataset_filename, 'rb') as f:
            reader = csv.reader(f, delimiter=delimiter, quoting=quoting)
            if self.settings.get("dataset.randomize_file_reader"):
                data_matrix = self.randomized_read_lines(csv_reader, maximum_size)
            else:
                data_matrix = self.greedy_read_lines(reader, maximum_size)

        data_matrix, headers = self.detect_headers(data_matrix)
        data_types = DataTypeClassification.classify_data_matrix(data_matrix)
        data_matrix = DatasetCleaner(self.settings, data_matrix, headers).clean()
        self.logger.info("Read dataset from file: '%s'", self.dataset_filename)
        self.logger.info("Headers: %s", headers)
        self.logger.info("Dataset Size: %s", len(data_matrix))
        return Dataset(data_matrix, headers=headers, data_types=data_types)

    def detect_headers(self, data_matrix):
        """
        We look to see if there are any headers in the first row of the data_matrix.
        We check to make sure that all data types in the first row are either strings
        or booleans (because booleans can have "t", "true", etc. which could
        potentially be a header).

        If all data types in the first row are either strings or booleans, we check
        to make sure that the second row does not match exactly the first row. If
        both rows match, then we assume there were no headers. Otherwise we return
        the first row as headers.
        """
        if len(data_matrix) <= 1:
            return (data_matrix, None)

        header_data_types = DataTypeClassification.classify_row(data_matrix[0])
        row_data_types = DataTypeClassification.classify_data_matrix(data_matrix[1:])

        non_matching_types = 0
        for header_type, row_type in zip(header_data_types, row_data_types):
            if header_type.data_type in ["boolean", "string"]:
                if header_type.data_type != row_type:
                    non_matching_types += 1
            else:
                # Header type is not a boolean or string --  we assume that
                # this data_matrix doesn't have any headers.
                return (data_matrix, None)

        # If all header and first row types are matching, then we assume we don't
        # have any headers. Otherwise, we return the first row as headers.
        if non_matching_types == 0:
            return (data_matrix, None)
        else:
            headers = data_matrix.pop(0)
            return (data_matrix, headers)

    def greedy_read_lines(self, csv_reader, maximum_size):
        data_matrix = []
        for row in csv_reader:
            data_matrix.append(row)

            if len(data_matrix) >= maximum_size:
                break

        return data_matrix

    def randomized_read_lines(self, csv_reader, maximum_size):
        data_matrix = []
        count = 0
        for row in csv_reader:
            count += 1
            if count > maximum_size:
                if random.random() < (float(maximum_size) / count):
                    replaced_index = random.randrange(maximum_size)
                    data_matrix[replaced_index] = row
            else:
                data_matrix.append(row)
        return data_matrix
