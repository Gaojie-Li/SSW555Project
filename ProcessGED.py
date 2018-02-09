import os
from collections import defaultdict


def process_ged(input_path, output_path):
    if input_path.endswith('.ged'):
        file = input_path
    else:
        raise TypeError('Please enter a path to a GED file.')

    tag_dict = defaultdict(str)
    tag_dict = {'INDI': '0', 'NAME': '1', 'SEX': '1', 'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1', 'FAM': '0',
                'MARR': '1', 'HUSB': '1', 'WIFE': '1', 'CHIL': '1', 'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}

    month_set = {'JAN', 'FEB', 'MAR', 'APR', 'MAY',
                 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'}

    writable = open(output_path, 'w')
    readable = open(file)

    for line in readable:
        line = line.strip()
        writable.write('--> ' + line + '\n')
        items = line.split(' ')

        level = items[0]
        tag = ''
        arguments = ''
        valid = True

        # case for INDI and FAM
        if len(items) > 2 and (items[2] == 'INDI' or items[2] == 'FAM'):
            tag = items[2]
            arguments = items[1]
        else:
            tag = items[1]
            if tag == 'INDI' or tag == 'FAM':
                valid = False

            if tag == 'DATE':
                # items[2]: day, items[3]: month, items[4]: year
                if len(items) != 5 or items[2][0] == '0' or items[3] not in month_set or len(items[4]) != 4 or not items[4].isnumeric():
                    valid = False

            if tag == 'NAME':
                lastName = items[len(items) - 1]
                if not lastName.startswith('/') or not lastName.endswith('/'):
                    valid = False

            for i, item in enumerate(items):
                if i > 1:
                    arguments += item + ' '

        writable.write('<-- ' + level + '|' + tag + '|' + (
            'Y' if valid and tag in tag_dict and level in tag_dict[tag] else 'N') + (('|' + arguments + '\n') if len(arguments) > 0 else ('\n')))

    writable.close()
    readable.close()


process_ged('./proj02test.ged', 'test.txt')
process_ged('./GEDCOMFile_GaojieLi.ged', 'my_tree.txt')
