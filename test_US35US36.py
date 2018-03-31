import unittest
import ProcessResult as pr
from collections import defaultdict


class us3536_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)

    indi_id1 = 'I23'
    detail1 = {'NAME': 'Yifeng /Li/', 'SEX': 'M',
               'BIRT': '2018-03-06', 'FAMS': ',F9'}

    indi_id2 = 'I6'
    detail2 = {'NAME': 'Dongbin /Lu/', 'SEX': 'M',
               'BIRT': '1927-07-06', 'DEAT': '2018-03-10', 'FAMS': ',F3'}

    indi_id3 = 'I25'
    detail3 = {'NAME': 'dada /Li/', 'SEX': 'M',
               'BIRT': '2018-03-22', 'FAMC': ',F9'}

    indi_dict[indi_id1] = detail1
    indi_dict[indi_id2] = detail2
    indi_dict[indi_id3] = detail3

    def test_35_true_case(self):
        self.assertEqual(pr.list_recent_births(self.indi_dict), {'I23': [
                         'Yifeng /Li/', '2018-03-06', 25], 'I25': ['dada /Li/', '2018-03-22', 9]})

    def test_36_true_case(self):
        self.assertEqual(pr.list_recent_deaths(self.indi_dict), {'I6': [
                         'Dongbin /Lu/', '2018-03-10', 21]})


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
