import unittest
import ProcessResult as pr
from collections import defaultdict


class us10_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    indi_dict.update({'I1': {'BIRT': '1970-10-00'}
                    , 'I2': {'BIRT': '1990-10-10'}

                    , 'I3': {'BIRT': '1980-10-00'}
                    , 'I4': {'BIRT': '1990-10-10'}
                })
    
    fam_dict = defaultdict(defaultdict)
    fam_dict.update({'F1': {'HUSB': 'I1', 'WIFE': 'I2', 'MARR': '2004-10-11'}
                    ,'F2': {'HUSB': 'I3', 'WIFE': 'I4', 'MARR': '2004-10-09'}
                })

    def test_ill_age(self):
        res = pr.marriage_after_14(self.indi_dict, self.fam_dict)
        self.assertIn('ERROR', res)
        self.assertIn('F2', res)


class us18_test(unittest.TestCase):
    indi_dict = defaultdict(defaultdict)
    indi_dict.update({'I1': {'FAMS': 'F2'}, 'I2': {'FAMS': 'F2'}})

    fam_dict = defaultdict(defaultdict)
    fam_dict.update({'F1': {'CHIL': 'I1,I2'}})

    def test_ill_marriage(self):
        res = pr.siblings_no_marriage(self.indi_dict, self.fam_dict)
        self.assertIn('ERROR', res)
        self.assertIn('F1', res)
    

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)