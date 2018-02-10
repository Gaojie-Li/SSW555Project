import os
from prettytable import PrettyTable
from collections import defaultdict

month_lib = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05',
             'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

this_year = 2018

tag_w_extension = {'BIRT', 'DEAT', 'MARR', 'DIV'}


def parse_line(line):
    items = line.strip('<-- \n').split('|')
    # print(items)
    return (items[0], items[1], items[2], items[3] if len(items) > 3 else None)


""" Method to parse date input into desired format """


def parse_date(date_str):
    date = date_str.split(' ')
    day = date[0]
    month = date[1]
    year = date[2]

    return year + '-' + month_lib[month] + '-' + day

# read level 2


def get_data_of_property(readable, i):
    date = ''
    while i < len(readable):
        line = readable[i]

        if line.startswith('--> '):
            i += 1
            continue

        # 2|DATE|Y|19 MAR 2015
        level, tag, valid, args = parse_line(line)

        i += 1

        # invalid cases
        if valid == 'N':
            continue
        if level != '2':
            break

        if tag == 'DATE':
            date = parse_date(args)

    return date, i - 1

# read level 1


def get_properties(readable, i):
    dd = defaultdict(str)

    while i < len(readable):
        line = readable[i]

        if line.startswith('--> '):
            i += 1
            continue

        # 1 NAME Zheng /Li/
        level, tag, valid, args = parse_line(line)
        # print(line)

        i += 1

        if valid == 'N':
            continue
        if level != '1':
            break

        if tag in tag_w_extension:
            # passed in line i is the line w/ level 2
            # returned line i is the line w/ level 1
            dd[tag], i = get_data_of_property(readable, i)
        else:
            dd[tag] = args.strip('@\n ')

    return dd, i - 1

# read level 0


def process_result(input_path):
    if input_path.endswith('.txt'):
        file = input_path
    else:
        raise TypeError('Please enter a path to a txt file.')

    readable = open(file).readlines()

    # key: id
    individual_dict = defaultdict(defaultdict)
    family_dict = defaultdict(defaultdict)

    i = 0
    # read all individual data
    while i < len(readable):
        line = readable[i]
        if line.startswith('--> '):
            i += 1
            continue

        # 0|FAM|Y|@F6@ ORRRR 0|INDI|Y|@I8@
        level, tag, valid, args = parse_line(line)

        i += 1

        # if not valid
        if 'N' == valid or args is None or level != '0':
            continue

        object_id = args.strip('@\n ')
        # passed in line i is the line with level 1
        # returned line i is the line with level 0
        if tag == 'FAM':
            family_dict[object_id], i = get_properties(readable, i)
        elif tag == 'INDI':
            individual_dict[object_id], i = get_properties(readable, i)

    # read all family data

    individual_table = PrettyTable(field_names=[
                                   'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    for person_id, value in individual_dict.items():
        age = (this_year - int(value['BIRT'].split('-')[0])) if 'DEAT' not in value else (
            int(value['DEAT'].split('-')[0]) - int(value['BIRT'].split('-')[0]))
        alive = 'True' if 'DEAT' not in value else 'False'
        death = value['DEAT'] if 'DEAT' in value else 'NA'
        child = ('{\'' + value['FAMC'] + '\'}') if 'FAMC' in value else 'NA'
        spouse = ('{\'' + value['FAMS'] + '\'}') if 'FAMS' in value else 'NA'

        individual_table.add_row(
            [person_id, value['NAME'], value['SEX'], value['BIRT'], age, alive, death, child, spouse])

    print(individual_table)

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])


process_result('./result.txt')
