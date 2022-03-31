import csv


def load_csv(file_path):
    """
    loading a csv file
    :param file_path: filepath string
    :return: list of list
    """
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        return [i for i in csv_reader]