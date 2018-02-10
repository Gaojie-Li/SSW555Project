import os
from prettytable import PrettyTable
from collections import defaultdict

TRANS_TAGS = {'DATE': 'Date'}


def parse_line(line):
    items = line.lstrip('<-- ').split('|')
    return (items[0], items[1], items[2], items[3] if len(items) > 3 else None)


# read level 2
def get_data_of_property(readable, i):
    cur_item = defaultdict(str)

    while i < len(readable):
        line = readable[i]
        level, tag, valid, args = parse_line(line)

        # invalid cases
        if valid == 'N':
            continue
        if level == '1':
            break

        cur_item[tag] = args

    return cur_item, i

# read level 1


def get_properties(readable, i):
    dd = defaultdict(str)

    while i < len(readable):
        line = readable[i]
        # 1 NAME Zheng /Li/
        level, tag, valid, args = parse_line(line)

        if '0' == level:
            break

        i += 1

        if '1' != level or 'N' == valid:
            continue

        dd[tag], i = get_data_of_property(readable, i)

    return dd, i

# read level 0


def process_result(input_path, output_path):
    if input_path.endswith('.txt'):
        file = input_path
    else:
        raise TypeError('Please enter a path to a txt file.')

    readable = open(file).readlines()

    # key: id
    individual_dict = defaultdict(defaultdict(str))
    family_dict = defaultdict(defaultdict(str))

    i = 0
    # read all individual data
    while i < len(readable):
        line = readable[i]
        if line.startswith('-->'):
            continue

        level, tag, valid, args = parse_line(line)

        if tag == 'FAM':
            break
        # if not valid
        if 'N' == valid:
            continue

        # if not INDI or FAM
        if not (0 == level and 'INDI' == tag):
            continue

        indi_id = args.strip('@')
        individual_dict[indi_id], i = get_properties(readable, i)

    # read all family data

    individual_table = PrettyTable(field_names=[
                                   'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])


process_result('./test.txt', './output.txt')
