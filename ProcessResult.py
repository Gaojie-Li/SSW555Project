import os
from prettytable import PrettyTable
from collections import defaultdict

TRANS_TAGS = {'DATE': Name}

def parse_line(line):
    items = line.lstrip('<-- ').split('|')
    return (int(items[0]), items[1], items[2], items[3] if len(items) > 3 else None)

def get_data_of_property(readable, i):
    while i < len(readable):
        line = readable[i]
        level, tag, valid, args = parse_line(line)

        if 


def get_properties(readable, i):
    dd = defaultdict(str)

    while i < len(readable):
        line = readable[i]
        level, tag, valid, args = parse_line(line)

        if 0 == level:
            break

        i += 1

        if 1 != level or 'N' == valid:
            continue

        dd[tag], i = get_data_of_property(readable, i)

    return dd, i


def process_result(input_path, output_path):
    if input_path.endswith('.txt'):
        file = input_path
    else:
        raise TypeError('Please enter a path to a txt file.')

    readable = open(file).readlines()

    individual_dict = defaultdict(defaultdict(str))
    family_dict = defaultdict(defaultdict(str))

    i = 0
    while i < len(readable):
        line = readable[i]
        if line.startswith('-->'):
            continue

        level, tag, valid, args = parse_line(line)
        if 'N' == valid:
            continue

        if not (0 == level and 'INDI' == tag):
            continue
        
        indi_id = args.strip('@')
        individual_dict[indi_id], i = get_properties(readable, i)




        individual_dict




    individual_table = PrettyTable(field_names=[
                                   'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])


process_result('./test.txt', './output.txt')
