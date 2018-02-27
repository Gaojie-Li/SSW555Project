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
        age = (THIS_YEAR - int(value['BIRT'].split('-')[0])) if 'DEAT' not in value else (
            int(value['DEAT'].split('-')[0]) - int(value['BIRT'].split('-')[0]))
        alive = 'True' if 'DEAT' not in value else 'False'
        death = value['DEAT'] if 'DEAT' in value else 'NA'
        child = ('{' + ', '.join([repr(s) for s in set(value['FAMC'].strip(
            ',').split(','))]) + '}') if 'FAMC' in value else 'NA'
        spouse = ('{' + ', '.join([repr(s) for s in set(
            value['FAMS'].strip(',').split(','))]) + '}') if 'FAMS' in value else 'NA'

        individual_table.add_row(
            [person_id, value['NAME'], value['SEX'], value['BIRT'], age, alive, death, child, spouse])

    writable.write('Individuals\n')
    writable.write(str(individual_table) + '\n')

    family_table = PrettyTable(field_names=[
                               'ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])

    #TODO: family_table.add_row
    for fam_id, value in fam_dict.items():
        married = value['MARR'] if 'MARR' in value else 'NA'
        divorced = value['DIV'] if 'DIV' in value else 'NA'
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


# acceptance_test(indi_dict, fam_dict)
acceptance_test()
