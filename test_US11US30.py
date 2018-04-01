import unittest
import ProcessResult
from collections import defaultdict


class us11us30_test(unittest.TestCase):
    indi_i1 = defaultdict(str)
    indi_i1['FAMS'] = 'F1,F2'
    indi_i2 = defaultdict(str)
    indi_i2['BIRT'] = '2020-06-24'
    indi_i2['FAMC'] = 'F2'
    i2_dad = defaultdict(str)
    i2_dad['DEAT'] = '1995-02-10'

    indi_dict = defaultdict(defaultdict)
    indi_dict['I1'] = indi_i1
    indi_dict['I2'] = indi_i2
    indi_dict['I3'] = i2_dad

    fam_dict = defaultdict(defaultdict)
    fam_f1 = defaultdict(str)
    fam_f1['MARR'] = '1962-09-08'
    fam_f1['DIV'] = '1982-02-15'
    fam_dict['F1'] = fam_f1
    fam_f2 = defaultdict(str)
    fam_f2['MARR'] = '1973-05-20'
    fam_dict['F2'] = fam_f2

    def test_11_false_case(self):
        self.assertEqual(ProcessResult.no_bigamy('I1', self.indi_dict, self.fam_dict),
                         'ERROR: FAMILY: US11: I1 is having a bigamy in F1 and F2!')

    def test_30_case(self):
        self.assertEqual(ProcessResult.list_living_married(
            self.indi_dict, self.fam_dict), ['I1'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
