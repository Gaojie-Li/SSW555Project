from collections import defaultdict
import ProcessGED
import ProcessResult as pr


def acceptance_test():
    ProcessGED.process_ged('./tree.ged', './ged_result.txt')
    indi_dict, fam_dict = pr.process_result('./ged_result.txt')

# # key: 1-6, value: pr.divorce_before_death
    quiry_service = {1: pr.date_before_today, 2: pr.birth_before_marriage, 3: pr.birth_before_death,
                     4: pr.marriage_before_divorce, 5: pr.marriage_before_death, 6: pr.divorce_before_death}

    for indi in indi_dict:
        for test_index in range(1, 7):
            quiry_service[test_index](indi, indi_dict, fam_dict)


# acceptance_test(indi_dict, fam_dict)
acceptance_test()
