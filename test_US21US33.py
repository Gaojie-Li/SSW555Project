import unittest
from collections import defaultdict
import ProcessResult as pr


class test_US21US33(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    indi_dict.update({
        'I1': {'NAME': 'Andy', 'BIRT': '1997-12-6', 'FAMC': 'F1'},
        'I2': {'NAME': 'Dad', 'DEAT': '2000-05-17', 'SEX': 'F', 'FAMS': 'F1'},
        'I3': {'NAME': 'Mom', 'DEAT': '2010-08-15', 'SEX': 'M', 'FAMS': 'F1'}
    })

    fam_dict = defaultdict(defaultdict)
    fam_dict.update({
        'F1': {'HUSB': 'I2', 'WIFE': 'I3', 'CHIL': 'I1'}
    })

    def test_us21_with_orphan(self):
        self.assertEqual(pr.list_orphans(
            self.indi_dict, self.fam_dict), {'I1': 'Andy'})

    def test_us33_invalid(self):
        self.assertEqual(pr.correct_gender_for_role(self.indi_dict, self.fam_dict), {
                         'F1': 'Gender in correct for either husband or wife.'})


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
