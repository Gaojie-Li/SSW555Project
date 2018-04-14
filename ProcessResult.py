import os
from prettytable import PrettyTable
from collections import defaultdict
from datetime import datetime
from datetime import date
from collections import deque

MONTH_LIB = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05',
             'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12',
             '00': '00'  # US41
             }

THIS_YEAR = 2018

TAG_W_EXTENSION = {'BIRT', 'DEAT', 'MARR', 'DIV'}


def parse_line(line):
    items = line.strip('<-- \n').split('|')
    # print(items)
    return (items[0], items[1], items[2], items[3] if len(items) > 3 else None)


""" Method to parse date input into desired format """


def parse_date(date_str):
    date = date_str.strip().split(' ')

    if len(date) and len(date) < 3:
        tmp_date = []
        for _ in range(3 - len(date)):
            tmp_date.append('00')
        tmp_date.extend(date)
        date = tmp_date

    day = date[0]
    month = date[1]
    year = date[2]

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

    return individual_dict, family_dict


""" Helper function to find relationship between two dates """


def is_before(date1, date2):
    if int(date1[0]) < int(date2[0]):
        return True
    if int(date1[0]) == int(date2[0]) and int(date1[1]) < int(date2[1]):
        return True
    if int(date1[0]) == int(date2[0]) and int(date1[1]) == int(date2[1]) and int(date1[2]) < int(date2[2]):
        return True

    return False


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
        if is_before(marry_date, birth_date):
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
        if is_before(death_date, divorce_date):
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
    if is_before(death_date, birth_date):
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
        if is_before(death_date, marriage_date):
            return "ERROR: INDIVIDUAL: US05: {}: Marriage date {} is after death date {}!".format(
                indi_id, m_date, indi_dict[indi_id]['DEAT'])

    return True


def is_after_today(date_list):
    iyear = int(date_list[0])
    imonth = int(date_list[1])
    iday = int(date_list[2])
    return datetime(iyear, imonth if imonth != 0 else 1, iday if iday != 0 else 1).date() > datetime.now().date()


def date_before_today(indi_id, indi_dict, fam_dict):
    ''' US01: Dates before current date
    '''
    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if type(fam_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'

    if 'BIRT' in indi_dict[indi_id]:
        birth_date = indi_dict[indi_id]['BIRT'].split('-')
        if is_after_today(birth_date):
            return "ERROR: INDIVIDUAL: US01: {}: Birth date {} is after today!".format(
                indi_id, indi_dict[indi_id]['BIRT'])

    if 'DEAT' in indi_dict[indi_id]:
        death_date = indi_dict[indi_id]['DEAT'].split('-')
        if is_after_today(death_date):
            return "ERROR: INDIVIDUAL: US01: {}: Death date {} is after today!".format(
                indi_id, indi_dict[indi_id]['DEAT'])

    # check Marry & Divorce dates
    if 'FAMS' not in indi_dict[indi_id]:
        return True

    fams = indi_dict[indi_id]['FAMS'].strip(',').split(',')
    for fam_id in fams:
        if 'MARR' in fam_dict[fam_id]:
            marr_date = fam_dict[fam_id]['MARR'].split('-')
            if is_after_today(marr_date):
                return "ERROR: FAMILY: US01: {} {}: Marriage date {} is after today!".format(
                    indi_id, fam_id, fam_dict[fam_id]['MARR'])

        if 'DIV' in fam_dict[fam_id]:
            div_date = fam_dict[fam_id]['DIV'].split('-')
            if is_after_today(div_date):
                return "ERROR: FAMILY: US01: {} {}: Divorce date {} is after today!".format(
                    indi_id, fam_id, fam_dict[fam_id]['DIV'])

    return True


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

        div_ymd = ((int(field) if field != '00' else 1)
                   for field in fam_dict[fam_id]['DIV'].split('-'))
        mar_ymd = ((int(field) if field != '00' else 1)
                   for field in fam_dict[fam_id]['MARR'].split('-'))

        if datetime(*div_ymd) < datetime(*mar_ymd):
            return "ERROR: FAMILY: US04: {} {}: Divorce date {} is before marriage date {}!".format(
                indi_id, fam_id, fam_dict[fam_id]['DIV'], fam_dict[fam_id]['MARR'])


def order_siblings_by_age(indi_dict, fam_dict):
    ''' US28: Order siblings by age
    '''
    if type(indi_dict) != defaultdict:
        return "Only defaultdict is acceptable"
    if type(fam_dict) != defaultdict:
        return "Only defaultdict is acceptable"

    dd = defaultdict(list)

    for fam_id in fam_dict:
        children = fam_dict[fam_id].get('CHIL', '')

        if '' == children:
            children = ['NA']
        else:
            children = children.strip(',').split(',')
            # for id in children:
            #     print(indi_dict[id]['BIRT'])
            children = sorted(children, key=lambda indi_id: datetime(
                *((int(ymd) if ymd != '00' else 1) for ymd in indi_dict[indi_id]['BIRT'].split('-'))))

        dd[fam_id].extend(children)

    return dd


""" US08 Birth before marriage of parents """


def birth_before_marriage_of_parents(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMC' not in indi_dict[indi_id]:
        return 'The person is not child of any family.'

    birth_date = indi_dict[indi_id]['BIRT'].split('-')
    famc = indi_dict[indi_id]['FAMC'].strip(',')
    marry_date = fam_dict[famc]['MARR'].split('-')

    if is_before(birth_date, marry_date):
        return "ERROR: INDIVIDUAL: US08: {}: Birth date {} is before marriage date of their parents {}!".format(
            indi_id, indi_dict[indi_id]['BIRT'], fam_dict[famc]['MARR'])

    return True


""" US09 Birth before death of parents """


def birth_before_death_of_parents(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMC' not in indi_dict[indi_id]:
        return 'The person is not child of any family.'

    birth_date = indi_dict[indi_id]['BIRT'].split('-')
    famc = indi_dict[indi_id]['FAMC'].strip(',')

    dates = [indi_dict[fam_dict[famc]['HUSB']]['DEAT'] if 'DEAT' in indi_dict[fam_dict[famc]['HUSB']] else "",
             indi_dict[fam_dict[famc]['WIFE']]['DEAT'] if 'DEAT' in indi_dict[fam_dict[famc]['WIFE']] else ""]

    for date in dates:
        if date != "":
            split_date = date.split('-')
            if is_before(split_date, birth_date):
                return "ERROR: INDIVIDUAL: US09: {}: Birth date {} is after death date of his/her parents {}!".format(
                    indi_id, indi_dict[indi_id]['BIRT'], date)

    return True


""" US29 List deceased """


def list_deceased(indi_dict):
    if type(indi_dict) != defaultdict:
        return 'Invalid dictionary type.'

    dd = defaultdict(list)
    for indi_id in indi_dict:
        if 'DEAT' in indi_dict[indi_id]:
            detail = []
            detail.append(indi_dict[indi_id]['NAME'])
            detail.append(indi_dict[indi_id]['DEAT'])
            dd[indi_id] = detail

    return dd


""" US31 list living single """


def list_living_single(indi_dict):
    if type(indi_dict) != defaultdict:
        return 'Invalid dictionary type.'

    dd = defaultdict(list)
    cur_year = 2018

    for indi_id in indi_dict:
        if 'DEAT' not in indi_dict[indi_id] and 'FAMS' not in indi_dict[indi_id]:
            date = indi_dict[indi_id]['BIRT'].split('-')
            if(cur_year - int(date[0]) > 30):
                detail = []
                detail.append(indi_dict[indi_id]['NAME'])
                detail.append(cur_year - int(date[0]))
                dd[indi_id] = detail
    return dd


""" US35 list recent births """


def list_recent_births(indi_dict):
    if type(indi_dict) != defaultdict:
        return "Invalid dictionary type"
    dd = defaultdict(list)
    cur_year = 2018
    cur_month = 3
    cur_day = 31
    cur_date = date(cur_year, cur_month, cur_day)
    for indi_id in indi_dict:
        birth_date = indi_dict[indi_id]['BIRT'].split('-')
        birth_year = int(birth_date[0])

        birth_month = 0
        if birth_date[1].startswith('0'):
            birth_month = int(birth_date[1][1:])
        else:
            birth_month = int(birth_date[1])

        birth_day = 0
        if birth_date[2].startswith('0'):
            birth_day = int(birth_date[2][1:])
        else:
            birth_day = int(birth_date[2])

        if birth_year == 0 or birth_year > cur_year or birth_month == 0 or birth_day == 0:
            continue

        d0 = date(birth_year, birth_month, birth_day)
        delta = cur_date - d0

        if delta.days <= 30:
            detail = []
            detail.append(indi_dict[indi_id]['NAME'])
            detail.append(indi_dict[indi_id]['BIRT'])
            detail.append(delta.days)
            dd[indi_id] = detail
    return dd


""" US36 list recent deaths """


def list_recent_deaths(indi_dict):
    if type(indi_dict) != defaultdict:
        return "Invalid dictionary type"
    dd = defaultdict(list)
    cur_year = 2018
    cur_month = 3
    cur_day = 31
    cur_date = date(cur_year, cur_month, cur_day)
    for indi_id in indi_dict:
        if 'DEAT' in indi_dict[indi_id]:
            death_date = indi_dict[indi_id]['DEAT'].split('-')
            death_year = int(death_date[0])

            death_month = 0
            if death_date[1].startswith('0'):
                death_month = int(death_date[1][1:])
            else:
                death_month = int(death_date[1])

            death_day = 0
            if death_date[2].startswith('0'):
                death_day = int(death_date[2][1:])
            else:
                death_day = int(death_date[2])

            if death_year == 0 or death_year > cur_year or death_month == 0 or death_day == 0:
                continue

            d0 = date(death_year, death_month, death_day)
            delta = cur_date - d0

            if delta.days <= 30:
                detail = []
                detail.append(indi_dict[indi_id]['NAME'])
                detail.append(indi_dict[indi_id]['DEAT'])
                detail.append(delta.days)
                dd[indi_id] = detail
    return dd


def large_age_diffs(indi_dict, fam_dict):
    ''' US34: List large age differences
    '''
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type'

    res = []

    for fam_id, value in fam_dict.items():
        husID = value['HUSB']
        husName = indi_dict[husID]['NAME']
        wifID = value['WIFE']
        wifName = indi_dict[wifID]['NAME']

        husBirt = [int(ymd) for ymd in indi_dict[husID]['BIRT'].split('-')]
        wifBirt = [int(ymd) for ymd in indi_dict[wifID]['BIRT'].split('-')]
        marr_date = [int(ymd) for ymd in fam_dict[fam_id]['MARR'].split('-')]
        # adjust all omitted fields of partial dates so that we can use datetime() to compare them:
        for i in range(2):
            if husBirt[2 - i] * wifBirt[2 - i] * marr_date[2 - i] == 0:
                # default month and/or day
                husBirt[2 - i] = wifBirt[2 - i] = marr_date[2 - i] = 1

        husAge = datetime(*marr_date) - datetime(*husBirt)
        wifAge = datetime(*marr_date) - datetime(*wifBirt)

        if husAge >= wifAge * 2 or wifAge >= husAge * 2:
            res.append(fam_id)

    return res


def siblings_spacing(indi_dict, fam_dict):
    ''' US13: Siblings spacing
    '''
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type'

    for fam_id in fam_dict:
        children = fam_dict[fam_id]['CHIL'].strip(',').split(',')
        coll = []
        for chil_id in children:
            e = [int(ymd) for ymd in indi_dict[chil_id]
                 ['BIRT'].split('-') if int(ymd) != 0]
            if len(e) == 3:  # to simplify, only check full dates!
                coll.append(datetime(*e))

        if len(coll) == 0:
            continue

        coll = sorted(coll)
        cmp_8m_base = coll[0]
        last_within_2d = 0
        from datetime import timedelta

        for i in range(len(coll)):
            if coll[i] - cmp_8m_base <= timedelta(days=2):
                pass
            elif coll[i] - coll[last_within_2d] >= timedelta(days=8 * 30 + 4):
                cmp_8m_base = coll[i]
            else:
                return "ERROR: FAMILY: US13: {}: A child's birth date {} is ill-spacing with previous child's birth date {}!".format(
                    fam_id, coll[i], coll[last_within_2d])

            last_within_2d = i

    return True


""" US 11: No Bigamy"""


def no_bigamy(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'
    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'
    if 'FAMS' not in indi_dict[indi_id]:
        return True

    marriage_dates = []
    divorce_dates = []
    fams = indi_dict[indi_id]['FAMS'].strip(',').split(',')
    if len(fams) < 2:
        return True

    for fam in fams:
        marriage_dates.append(fam_dict[fam]['MARR'])
        divorce_dates.append(
            fam_dict[fam]['DIV'] if 'DIV' in fam_dict[fam] else '9999-99-99')

    for i in range(len(marriage_dates)):
        for j in range(len(marriage_dates)):
            if j == i:
                continue
            if is_before(marriage_dates[i].split('-'), marriage_dates[j].split('-')):
                if is_before(marriage_dates[j].split('-'), divorce_dates[i].split('-')):
                    return "ERROR: FAMILY: US11: {} is having a bigamy in {} and {}!".format(
                        indi_id, fams[i], fams[j])
            elif is_before(marriage_dates[j].split('-'), marriage_dates[i].split('-')):
                if is_before(marriage_dates[i].split('-'), divorce_dates[j].split('-')):
                    return "ERROR: FAMILY: US11: {} is having a bigamy in {} and {}!".format(
                        indi_id, fams[i], fams[j])

    return True


""" US 30: List Living Married """


def list_living_married(indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'

    result = []
    for indi, value in indi_dict.items():
        if 'DEAT' in value or 'FAMS' not in value:
            continue
        result.append(indi)

    return result


""" US12: Parents not too old """


def parent_not_too_old(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'

    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'

    indi_birth = indi_dict[indi_id]['BIRT'].strip().split('-')

    if 'FAMC' in indi_dict[indi_id]:
        fam_id = indi_dict[indi_id]['FAMC'].strip(',')
        husb_id = fam_dict[fam_id]['HUSB']
        wife_id = fam_dict[fam_id]['WIFE']
        husb_birth = indi_dict[husb_id]['BIRT'].strip().split('-')
        wife_birth = indi_dict[wife_id]['BIRT'].strip().split('-')
        if (int(indi_birth[0]) - int(husb_birth[0])) > 80 or (int(indi_birth[0]) - int(wife_birth[0])) > 60:
            return 'ERROR: INDIVIDUAL: US12: Parens of {} are too old...'.format(indi_id)

    return True


""" US23: Unique name and birth date """


def unique_name_and_birth_date(indi_id, indi_dict, fam_dict):
    if type(indi_dict) != defaultdict or type(fam_dict) != defaultdict:
        return 'Invalid dictionary type.'

    if indi_id not in indi_dict:
        return 'Person doesn\'t exist in the database.'

    for indi in indi_dict:
        if indi != indi_id:
            if indi_dict[indi_id]['NAME'] == indi_dict[indi]['NAME'] and indi_dict[indi_id]['BIRT'] == indi_dict[indi]['BIRT']:
                return 'ERROR: INDIVIDUAL: US23: {} is the same person as {}'.format(indi_id, indi)

    return True
