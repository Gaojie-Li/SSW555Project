import unittest
import ProcessResult
from collections import defaultdict


class us0809_test(unittest.TestCase):
    indi_i1 = defaultdict(str)
    indi_i1['BIRT'] = '1988-08-28'
    indi_i1['FAMC'] = 'F1'
    indi_i2 = defaultdict(str)
    indi_i2['BIRT'] = '2020-06-24'
    indi_i2['FAMC'] = 'F2'
    i2_dad = defaultdict(str)
    i2_dad['DEAT'] = '1995-02-10'

    indi_dict = defaultdict(defaultdict)
    indi_dict['I1'] = indi_i1
    indi_dict['I2'] = indi_i2
    indi_dict['I3'] = i2_dad

    fam_f1 = defaultdict(str)
    fam_f1['MARR'] = '2020-09-08'
    fam_dict = defaultdict(defaultdict)
    fam_dict['F1'] = fam_f1
    fam_f2 = defaultdict(str)
    fam_f2['HUSB'] = 'I3'
    fam_f2['WIFE'] = 'I1'
    fam_dict['F2'] = fam_f2

    def test_08_false_case(self):
        self.assertEqual(ProcessResult.birth_before_marriage_of_parents('I1', self.indi_dict, self.fam_dict),
                         'ERROR: INDIVIDUAL: US08: I1: Birth date 1988-08-28 is before marriage date of their parents 2020-09-08!')

    def test_09_false_case(self):
        self.assertEqual(ProcessResult.birth_before_death_of_parents('I2', self.indi_dict, self.fam_dict),
                         'ERROR: INDIVIDUAL: US09: I2: Birth date 2020-06-24 is after death date of his/her parents 1995-02-10!')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
