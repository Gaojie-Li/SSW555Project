import os
from prettytable import PrettyTable
from collections import defaultdict
from datetime import datetime

MONTH_LIB = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05',
             'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

THIS_YEAR = 2018

TAG_W_EXTENSION = {'BIRT', 'DEAT', 'MARR', 'DIV'}


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

    # # print(date_str)
    # try:
    #     iday = int(day)
    #     imonth = int(MONTH_LIB[month])
    #     iyear = int(year)
    # except ValueError:
    #     print("ERROR: Date has got invalid day, month or year field! Please check the original data.")
    #     iday = 1
    #     imonth = 1
    #     iyear = 9999

    # dt = datetime(iyear, imonth, iday).date()
    # nowd = datetime.now().date()
    # if dt > nowd:
    #     print("ERROR: US01: DATE shall not after the current date!")
    #     return 'INVALID_DATE'

    return year + '-' + MONTH_LIB[month] + '-' + '{:0>2d}'.format(int(day))

# read level 2


def get_data_of_property(readable, i):
    date = ''
    while i < len(readable):
        line = readable[i]
        if line.startswith('--> '):
            i += 1
            continue

        # e.g. 2|DATE|Y|19 MAR 2015
        level, tag, valid, args = parse_line(line)
        i += 1

        if valid == 'N':
            continue

        if level != '2':
            break  # return to parent level

        if tag == 'DATE':
            date = parse_date(args)

    return date, i - 1

# read level 1


# def check_marrdiv_date(dd):
#     if ('DIV' not in dd) or ('MARR' not in dd):
#         return -1  # non-checking context

#     div_date = dd['DIV']
#     mar_date = dd['MARR']

#     div_ymd = (int(field) for field in div_date.split('-'))
#     mar_ymd = (int(field) for field in mar_date.split('-'))

#     if datetime(*div_ymd) < datetime(*mar_ymd):
#         print('ERROR: US04: MARR.DATE shall not after DIV.DATE')
#         return 1

#     return 0


def get_properties(readable, i):
    dd = defaultdict(str)

    while i < len(readable):
        line = readable[i]
        if line.startswith('--> '):
            i += 1
            continue

        # e.g. 1 NAME Zheng /Li/
        level, tag, valid, args = parse_line(line)
        # print(line)
        i += 1

        if valid == 'N':
            continue

        if level != '1':
            assert(level == '0')
            break  # level == 0

        if tag in TAG_W_EXTENSION:
            # passed in line i is the line w/ level 2
            # returned line i is the line w/ level 1
            dd[tag], i = get_data_of_property(readable, i)

            # if 'DIV' == tag:
            #     if check_marrdiv_date(dd) > 0:
            #         print("\tDetails: marriage={}, divorce={}".format(
            #             dd['MARR'], dd['DIV']))

        elif tag not in ['FAMC', 'FAMS', 'CHIL']:
            dd[tag] = args.strip('@\n ')
        else:
            dd[tag] = ','.join([dd[tag], args.strip('@\n ')])

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
        if ('N' == valid) or (args is None) or (level != '0'):
            continue

        object_id = args.strip('@\n ')
        # passed in line i is the line with level 1
        # returned line i is the line with level 0
        if tag == 'FAM':
            family_dict[object_id], i = get_properties(readable, i)
        elif tag == 'INDI':
            individual_dict[object_id], i = get_properties(readable, i)

    # read all family data

    # writable = open('output.txt', 'w')
    # individual_table = PrettyTable(field_names=[
    #                                'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    # for person_id, value in individual_dict.items():
    #     age = (THIS_YEAR - int(value['BIRT'].split('-')[0])) if 'DEAT' not in value else (
    #         int(value['DEAT'].split('-')[0]) - int(value['BIRT'].split('-')[0]))
    #     alive = 'True' if 'DEAT' not in value else 'False'
    #     death = value['DEAT'] if 'DEAT' in value else 'NA'
    #     child = ('{' + ', '.join([repr(s) for s in set(value['FAMC'].strip(
    #         ',').split(','))]) + '}') if 'FAMC' in value else 'NA'
    #     spouse = ('{' + ', '.join([repr(s) for s in set(
    #         value['FAMS'].strip(',').split(','))]) + '}') if 'FAMS' in value else 'NA'

    #     individual_table.add_row(
    #         [person_id, value['NAME'], value['SEX'], value['BIRT'], age, alive, death, child, spouse])

    # writable.write('Individuals\n')
    # print('Individuals')
    # print(individual_table)
    # writable.write(str(individual_table))

    # family_table = PrettyTable(field_names=[
    #                            'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])

    # #TODO: family_table.add_row
    # for fam_id, value in family_dict.items():
    #     married = value['MARR'] if 'MARR' in value else 'NA'
    #     divorced = value['DIV'] if 'DIV' in value else 'NA'
    #     husID = value['HUSB']
    #     husName = individual_dict[husID]['NAME']
    #     wifID = value['WIFE']
    #     wifName = individual_dict[wifID]['NAME']
    #     children = ('{' + ', '.join([repr(s) for s in set(
    #         value['CHIL'].strip(',').split(','))]) + '}') if 'CHIL' in value else 'NA'

    #     family_table.add_row(
    #         [fam_id, married, divorced, husID, husName, wifID, wifName, children])

    # writable.write('Families\n')
    # print('Families')
    # writable.write(str(family_table))
    # print(family_table)

    return individual_dict, family_dict


def birth_before_marriage(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMS' not in indi_dict[indi_id]:
        return 'The person has not married.'

    birth_date = indi_dict[indi_id]['BIRT'].split('-')
    fams_list = indi_dict[indi_id]['FAMS'].strip(',').split(',')

    for fam in fams_list:
        marry_date = fam_dict[fam]['MARR'].split('-')
        if int(marry_date[0]) < int(birth_date[0]):
            return "ERROR: INDIVIDUAL: US02: {}: Birth date {} is after marriage date {}!".format(
                indi_id, indi_dict[indi_id]['BIRT'], fam_dict[fam]['MARR'])
        if int(marry_date[0]) == int(birth_date[0]) and int(marry_date[1]) < int(birth_date[1]):
            return "ERROR: INDIVIDUAL: US02: {}: Birth date {} is after marriage date {}!".format(
                indi_id, indi_dict[indi_id]['BIRT'], fam_dict[fam]['MARR'])
        if int(marry_date[0]) == int(birth_date[0]) and int(marry_date[1]) == int(birth_date[1]) and int(marry_date[0]) == int(birth_date[0]) and int(marry_date[2]) < int(birth_date[2]):
            return "ERROR: INDIVIDUAL: US02: {}: Birth date {} is after marriage date {}!".format(
                indi_id, indi_dict[indi_id]['BIRT'], fam_dict[fam]['MARR'])

    return True


def divorce_before_death(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type entered.'
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMS' not in indi_dict[indi_id]:
        return 'The target has not married yet.'
    if 'DEAT' not in indi_dict[indi_id]:
        return True

    death_date = indi_dict[indi_id]['DEAT'].split('-')
    fam_list = indi_dict[indi_id]['FAMS'].strip(',').split(',')

    for fam_id in fam_list:
        if 'DIV' not in fam_dict[fam_id]:
            continue

        divorce_date = fam_dict[fam_id]['DIV'].split('-')
        if divorce_date[0] > death_date[0]:
            return "ERROR: INDIVIDUAL: US06: {}: Divorce date {} is after death date {}!".format(
                indi_id, fam_dict[fam_id]['DIV'], indi_dict[indi_id]['DEAT'])
        if divorce_date[0] == death_date[0] and divorce_date[1] > death_date[1]:
            return "ERROR: INDIVIDUAL: US06: {}: Divorce date {} is after death date {}!".format(
                indi_id, fam_dict[fam_id]['DIV'], indi_dict[indi_id]['DEAT'])
        if divorce_date[0] == death_date[0] and divorce_date[1] == death_date[1] and divorce_date[2] > death_date[2]:
            return "ERROR: INDIVIDUAL: US06: {}: Divorce date {} is after death date {}!".format(
                indi_id, fam_dict[fam_id]['DIV'], indi_dict[indi_id]['DEAT'])

    return True


def birth_before_death(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if indi_id not in indi_dict:
        return "The person you look up does not exist"

    # The person has no specific birth date & death date
    if 'BIRT' not in indi_dict[indi_id] and 'DEAT' not in indi_dict[indi_id]:
        return None

    # The format for the date is YYYY-mm-dd
    birth_date = indi_dict[indi_id]['BIRT'].split('-')
    # The person is stil alive
    if 'DEAT' not in indi_dict[indi_id]:
        return True

    death_date = indi_dict[indi_id]['DEAT'].split('-')
    if int(death_date[0]) < int(birth_date[0]):
        return "ERROR: INDIVIDUAL: US03: {}: Birth date {} is after death date {}!".format(
            indi_id, indi_dict[indi_id]['BIRT'], indi_dict[indi_id]['DEAT'])

    if int(death_date[0]) == int(birth_date[0]) and int(death_date[1]) < int(birth_date[1]):
        return "ERROR: INDIVIDUAL: US03: {}: Birth date {} is after death date {}!".format(
            indi_id, indi_dict[indi_id]['BIRT'], indi_dict[indi_id]['DEAT'])

    if int(death_date[0]) == int(birth_date[0]) and int(death_date[1]) == int(birth_date[1]) and int(death_date[2]) < int(birth_date[2]):
        return "ERROR: INDIVIDUAL: US03: {}: Birth date {} is after death date {}!".format(
            indi_id, indi_dict[indi_id]['BIRT'], indi_dict[indi_id]['DEAT'])

    return True


def marriage_before_death(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if type(fam_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if indi_id not in indi_dict:
        return "The person you look up does not exist"

    if 'DEAT' not in indi_dict[indi_id]:
        return True
    if 'FAMS' not in indi_dict[indi_id]:
        return True
    death_date = indi_dict[indi_id]['DEAT'].split('-')
    fams = indi_dict[indi_id]['FAMS'].strip(',').split(',')

    marry_date = []     # ['YYYY-MM-dd', 'YYYY-MM-dd]

    for fam in fams:
        marry_date.append(fam_dict[fam]['MARR'])

    for m_date in marry_date:
        marriage_date = m_date.split('-')
        if int(death_date[0]) < int(marriage_date[0]):
            return "ERROR: INDIVIDUAL: US05: {}: Marriage date {} is after death date {}!".format(
                indi_id, m_date, indi_dict[indi_id]['DEAT'])

        if int(death_date[0]) == int(marriage_date[0]) and int(death_date[1]) < int(marriage_date[1]):
            return "ERROR: INDIVIDUAL: US05: {}: Marriage date {} is after death date {}!".format(
                indi_id, m_date, indi_dict[indi_id]['DEAT'])

        if int(death_date[0]) == int(marriage_date[0]) and int(death_date[1]) == int(marriage_date[1]) and int(death_date[2]) < int(marriage_date[2]):
            return "ERROR: INDIVIDUAL: US05: {}: Marriage date {} is after death date {}!".format(
                indi_id, m_date, indi_dict[indi_id]['DEAT'])

    return True


def date_before_today(indi_id, indi_dict, fam_dict):
    ''' US01: Dates before current date
    '''
    # print("DJFIEJFIEJIFJIEJI")
    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if type(fam_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'

    nowd = datetime.now().date()

    if 'BIRT' in indi_dict[indi_id]:
        birth_date = indi_dict[indi_id]['BIRT'].split('-')

        iyear = int(birth_date[0])
        imonth = int(birth_date[1])
        iday = int(birth_date[2])

        dt = datetime(iyear, imonth, iday).date()
        if dt > nowd:
            return "ERROR: INDIVIDUAL: US01: {}: Birth date {} is after today!".format(
                indi_id, indi_dict[indi_id]['BIRT'])

    if 'DEAT' in indi_dict[indi_id]:
        death_date = indi_dict[indi_id]['DEAT'].split('-')

        iyear = int(death_date[0])
        imonth = int(death_date[1])
        iday = int(death_date[2])

        dt = datetime(iyear, imonth, iday).date()
        if dt > nowd:
            return "ERROR: INDIVIDUAL: US01: {}: Death date {} is after today!".format(
                indi_id, indi_dict[indi_id]['DEAT'])

    # check Marry & Divorce dates
    if 'FAMS' not in indi_dict[indi_id]:
        return True

    fams = indi_dict[indi_id]['FAMS'].strip(',').split(',')
    for fam_id in fams:
        if 'MARR' in fam_dict[fam_id]:
            marr_date = fam_dict[fam_id]['MARR'].split('-')

            iyear = int(marr_date[0])
            imonth = int(marr_date[1])
            iday = int(marr_date[2])

            dt = datetime(iyear, imonth, iday).date()
            if dt > nowd:
                return "ERROR: FAMILY: US01: {} {}: Marriage date {} is after today!".format(
                    indi_id, fam_id, fam_dict[fam_id]['MARR'])

        if 'DIV' in fam_dict[fam_id]:
            div_date = fam_dict[fam_id]['DIV'].split('-')

            iyear = int(div_date[0])
            imonth = int(div_date[1])
            iday = int(div_date[2])

            dt = datetime(iyear, imonth, iday).date()
            if dt > nowd:
                return "ERROR: FAMILY: US01: {} {}: Divorce date {} is after today!".format(
                    indi_id, fam_id, fam_dict[fam_id]['DIV'])


def marriage_before_divorce(indi_id, indi_dict, fam_dict):
    ''' US04: Marriage before divorce
    '''

    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if type(fam_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMS' not in indi_dict[indi_id]:
        return True

    fams = indi_dict[indi_id]['FAMS'].strip(',').split(',')

    for fam_id in fams:
        if 'DIV' not in fam_dict[fam_id] or 'MARR' not in fam_dict[fam_id]:
            continue

        div_ymd = (int(field) for field in fam_dict[fam_id]['DIV'].split('-'))
        mar_ymd = (int(field) for field in fam_dict[fam_id]['MARR'].split('-'))

        if datetime(*div_ymd) < datetime(*mar_ymd):
            return "ERROR: FAMILY: US04: {} {}: Divorce date {} is before marriage date {}!".format(
                indi_id, fam_id, fam_dict[fam_id]['DIV'], fam_dict[fam_id]['MARR'])
