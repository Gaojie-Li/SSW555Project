import unittest
import ProcessResult as pr
from collections import defaultdict


class us2931_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    indi_id1 = 'I6'
    detail1 = {'NAME': 'Dongbin /Lu/', 'SEX': 'M',
               'BIRT': '1927-07-06', 'DEAT': '1995-02-10', 'FAMS': ',F3'}
    indi_id2 = 'I23'
    detail2 = {'NAME': 'Yifeng /Li/', 'SEX': 'M',
               'BIRT': '1927-07-06', 'DEAT': '1972-02-15', 'FAMS': ',F9'}
    indi_id3 = 'I25'
    detail3 = {'NAME': 'dada /Li/', 'SEX': 'M',
               'BIRT': '1977-11-20', 'FAMC': ',F9'}
    indi_dict[indi_id1] = detail1
    indi_dict[indi_id2] = detail2
    indi_dict[indi_id3] = detail3

    def test__29_true_case(self):
        self.assertEqual(pr.list_deceased(self.indi_dict), {
                         'I6': ['Dongbin /Lu/', '1995-02-10'], 'I23': ['Yifeng /Li/', '1972-02-15']})

    def test_31_true_case(self):
        self.assertEqual(pr.list_living_single(self.indi_dict),
                         {'I25': ['dada /Li/', 41]})


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
