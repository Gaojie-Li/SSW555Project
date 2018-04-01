import unittest
import ProcessResult as pr
from collections import defaultdict


class us34_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    indi_dict.update({'I1': {'NAME': 'A1', 'BIRT': '1970-10-00'}
                    , 'I2': {'NAME': 'A2', 'BIRT': '1990-10-10'}

                    , 'I3': {'NAME': 'B1', 'BIRT': '1980-10-00'}
                    , 'I4': {'NAME': 'B2', 'BIRT': '1990-10-10'}
                })
    
    fam_dict = defaultdict(defaultdict)
    fam_dict.update({'F1': {'HUSB': 'I1', 'WIFE': 'I2', 'MARR': '2010-10-20'}
                    ,'F2': {'HUSB': 'I3', 'WIFE': 'I4', 'MARR': '2010-10-20'}
                })

    def test_husb_x2_older(self):
        res = pr.large_age_diffs(self.indi_dict, self.fam_dict)
        self.assertIn('F1', res)
        self.assertNotIn('F2', res)


class us13_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    fam_dict = defaultdict(defaultdict)
    fam_dict.update({'F1': {'CHIL': 'I1,I2,I3,I4,I5'}})

    def test_well_spacing(self):
        self.indi_dict.update(
            { 'I3': {'NAME': 'A3', 'BIRT': '2010-10-12'}
            , 'I1': {'NAME': 'A1', 'BIRT': '2010-10-00'} # partial date; impossible to determine, to be ignored
            , 'I5': {'NAME': 'A5', 'BIRT': '2010-10-10'}
            , 'I4': {'NAME': 'A4', 'BIRT': '2011-06-15'} # 8 months later from I3
            , 'I2': {'NAME': 'A2', 'BIRT': '2010-10-11'}
            })
        self.assertTrue(pr.siblings_spacing(self.indi_dict, self.fam_dict))
    
    def test_ill_spacing(self):
        self.indi_dict.update(
            { 'I3': {'NAME': 'A3', 'BIRT': '2010-10-22'} # ILL!
            , 'I1': {'NAME': 'A1', 'BIRT': '2010-10-00'}
            , 'I5': {'NAME': 'A5', 'BIRT': '2010-10-10'}
            , 'I4': {'NAME': 'A4', 'BIRT': '2011-06-15'}
            , 'I2': {'NAME': 'A2', 'BIRT': '2010-10-11'}
            })
        self.assertIn('ERROR', pr.siblings_spacing(self.indi_dict, self.fam_dict))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)