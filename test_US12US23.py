import unittest
import ProcessResult as pr
from collections import defaultdict


class us1223_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    fam_dict = defaultdict(defaultdict)

    indi_id1 = 'I3'
    detail1 = {'NAME': 'Zheng /Li/', 'SEX': 'M',
               'BIRT': '2050-01-01', 'FAMC': ',F1'}
    indi_id2 = 'I28'
    detail2 = {'NAME': 'Zheng /Li/', 'SEX': 'M',
               'BIRT': '2050-01-01', 'FAMC': ',F1'}

    indi_id3 = 'I1'
    detail3 = {'NAME': 'Hongbiao /Li/', 'SEX': 'M',
               'BIRT': '1968-11-25', 'FAMS': ',F1', 'FAMC': ',F2'}

    indi_id4 = 'I2'
    detail4 = {'NAME': 'Ping /Lu/', 'SEX': 'F',
               'BIRT': '1970-07-26', 'FAMS': ',F1', 'FAMC': ',F3'}

    fam_id1 = 'F1'
    fam_detail1 = {'HUSB': 'I1', 'WIFE': 'I2',
                   'CHIL': ',I3', 'MARR': '1992-04-10'}

    indi_dict[indi_id1] = detail1
    indi_dict[indi_id2] = detail2
    indi_dict[indi_id3] = detail3
    indi_dict[indi_id4] = detail4
    fam_dict[fam_id1] = fam_detail1

    def test_12_true_case(self):
        self.assertEqual(pr.parent_not_too_old('I3', self.indi_dict, self.fam_dict),
                         'ERROR: INDIVIDUAL: US12: Parens of I3 are too old...')

    def test_23_true_case(self):
        self.assertEqual(pr.unique_name_and_birth_date(
            'I3', self.indi_dict, self.fam_dict), 'ERROR: INDIVIDUAL: US23: I3 is the same person as I28')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
