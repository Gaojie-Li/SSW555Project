import os
from prettytable import PrettyTable
from collections import defaultdict


def parse_line(line):
    return line.lstrip('<-- ').split('|')


def process_result(input_path, output_path):
    if input_path.endswith('.txt'):
        file = input_path
    else:
        raise TypeError('Please enter a path to a txt file.')

    readable = open(file)

    individual_dict = defaultdict(defaultdict)
    family_dict = defaultdict(defaultdict)

    for line in readable:
        if line.startswith('-->'):
            continue

        items = parse_line(line)

    individual_table = PrettyTable(field_names=[
                                   'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])


process_result('./test.txt', './output.txt')
