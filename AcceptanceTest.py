from collections import defaultdict
import ProcessGED
import ProcessResult as pr
from prettytable import PrettyTable

THIS_YEAR = 2018


def acceptance_test():
    ProcessGED.process_ged('./tree.ged', './ged_result.txt')
    indi_dict, fam_dict = pr.process_result('./ged_result.txt')

    writable = open('TestResult.txt', 'w')

    individual_table = PrettyTable(field_names=[
                                   'ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    for person_id, value in indi_dict.items():
        birtd = value['BIRT'].split('-')
        deatd = value['DEAT'].split('-') if 'DEAT' in value else ['00', '00', '00']
        for _ in range(2):
            if birtd[-1] == '00':
                del birtd[-1]
            if deatd[-1] == '00':
                del deatd[-1]

        # print(birtd[0], deatd[0])
        age = (THIS_YEAR - int(birtd[0])) if 'DEAT' not in value else (int(deatd[0]) - int(birtd[0]))
        alive = 'True' if 'DEAT' not in value else 'False'
        death = '-'.join(deatd) if 'DEAT' in value else 'NA'
        child = ('{' + ', '.join([repr(s) for s in set(value['FAMC'].strip(
            ',').split(','))]) + '}') if 'FAMC' in value else 'NA'
        spouse = ('{' + ', '.join([repr(s) for s in set(
            value['FAMS'].strip(',').split(','))]) + '}') if 'FAMS' in value else 'NA'

        individual_table.add_row(
            [person_id, value['NAME'], value['SEX'], '-'.join(birtd), age, alive, death, child, spouse])

    writable.write('Individuals\n')
    writable.write(str(individual_table) + '\n')

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])

    for fam_id, value in fam_dict.items():
        marrd = value['MARR'].split('-') if 'MARR' in value else ['00', '00', '00']
        divod = value['DIV'].split('-') if 'DIV' in value else ['00', '00', '00']
        for _ in range(2):
            if marrd[-1] == '00':
                del marrd[-1]
            if divod[-1] == '00':
                del divod[-1]

        married = '-'.join(marrd) if 'MARR' in value else 'NA'
        divorced = '-'.join(divod) if 'DIV' in value else 'NA'
        husID = value['HUSB']
        husName = indi_dict[husID]['NAME']
        wifID = value['WIFE']
        wifName = indi_dict[wifID]['NAME']
        children = ('{' + ', '.join([repr(s) for s in set(
            value['CHIL'].strip(',').split(','))]) + '}') if 'CHIL' in value else 'NA'

        family_table.add_row(
            [fam_id, married, divorced, husID, husName, wifID, wifName, children])

    writable.write('Families\n')
    writable.write(str(family_table) + '\n')

# # key: 1-6, value: pr.divorce_before_death
    quiry_service = {1: pr.date_before_today, 2: pr.birth_before_marriage, 3: pr.birth_before_death,
                     4: pr.marriage_before_divorce, 5: pr.marriage_before_death, 6: pr.divorce_before_death}

    for indi in indi_dict:
        for test_index in range(1, 7):
            result = quiry_service[test_index](indi, indi_dict, fam_dict)
            if result != True and result != None and result.startswith('ERROR'):
                writable.write(result + '\n')

    #US28
    ordered_siblings_table = PrettyTable(field_names=['Family ID', 'Children'])
    ordered_siblings_dict = pr.order_siblings_by_age(indi_dict, fam_dict)

    for fam_id in fam_dict:
        ordered_siblings_table.add_row([fam_id, ', '.join(ordered_siblings_dict[fam_id])])

    writable.write('US28: List siblings from older to younger:\n')
    writable.write(str(ordered_siblings_table) + '\n')
    #end US28

# acceptance_test(indi_dict, fam_dict)
acceptance_test()
