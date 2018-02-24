from collections import defaultdict
import ProcessGED
import ProcessResult as pr


def acceptance_test(indi_dict, fam_dict):
    # key: 1-6, value: pr.divorce_before_death
    quiry_service = {3: pr.birth_before_death, 4: pr.marriage_before_death,
                     5: pr.birth_before_marriage, 6: pr.divorce_before_death}
    name = input(
        'Please input the name of the person you want to search (firstname lastname):')
    names = name.lower().split()
    name = names[0] + ' /' + names[1] + '/'

    ids = []
    for key, value in indi_dict.items():
        if value['NAME'].lower() == name:
            ids.append(key)

    if len(ids) == 0:
        return 'Person doesn\'t exist in the database.'

    test = input('\n1. Dates before current date\n2. Marriage before divorce\n3. Birth before death\n4. Marriage before death\n5. Birth before marriage\n6. Divorce before death\nPlease select the index of the item you want to test: ')

    for ID in ids:
        print(quiry_service[int(test)](ID, indi_dict, fam_dict))


ProcessGED.process_ged('./tree.ged', './ged_result.txt')
indi_dict, fam_dict = pr.process_result('./ged_result.txt')

acceptance_test(indi_dict, fam_dict)
