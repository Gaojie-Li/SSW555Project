import unittest
from collections import defaultdict

class TestUS01(unittest.TestCase):
    ''' US01: Dates before current date
    '''
    def setUp(self):
        from ProcessResult import date_before_today
        self.fn = date_before_today

    def tearDown(self):
        pass

    def test_US01_bad_indi_dict_type(self):
        fam_dict = defaultdict()
        self.assertTrue(self.fn('', 0, fam_dict) == "Only defaultdict is acceptable")
            
    def test_US01_bad_fam_dict_type(self):
        indi_dict = defaultdict()
        self.assertTrue(self.fn('', indi_dict, 0) == "Only defaultdict is acceptable")
        
    def test_US01_not_a_key(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {}})
        fam_dict = defaultdict()
        self.assertTrue(self.fn('IXX', indi_dict, fam_dict) == 'Person doesn\'t exist in the database.')

    def test_US01_ill_birt_date(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'BIRT': '3018-03-02'}})
        fam_dict = defaultdict()
        self.assertTrue('ERROR' in self.fn('I01', indi_dict, fam_dict))
        
    def test_US01_ill_deat_date(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'DEAT': '3018-03-02'}})
        fam_dict = defaultdict()
        self.assertTrue('ERROR' in self.fn('I01', indi_dict, fam_dict))
    
    def test_US01_good_date_without_fams(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'BIRT': '1900-03-02', 'DEAT': '2000-03-02'}})
        fam_dict = defaultdict()
        self.assertTrue(self.fn('I01', indi_dict, fam_dict))

    def test_US01_ill_marr_date(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'FAMS': 'F01'}})
        fam_dict = defaultdict()
        fam_dict.update({'F01': {'MARR': '2020-03-02'}})
        self.assertTrue('ERROR' in self.fn('I01', indi_dict, fam_dict))

    def test_US01_ill_div_date(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'FAMS': 'F01'}})
        fam_dict = defaultdict()
        fam_dict.update({'F01': {'DIV': '2020-03-02'}})
        self.assertTrue('ERROR' in self.fn('I01', indi_dict, fam_dict))

    def test_US01_fams_dates(self):
        indi_dict = defaultdict()
        indi_dict.update({'I01': {'FAMS': 'F01'}})
        fam_dict = defaultdict()
        fam_dict.update({'F01': {'MARR': '2000-03-02', 'DIV': '2010-03-02'}})
        self.assertTrue(self.fn('I01', indi_dict, fam_dict) == True)



# class TestUS04(unittest.TestCase):
#     def setUp(self):
#         from ProcessResult import check_marrdiv_date
#         self.fn = check_marrdiv_date

#     def tearDown(self):
#         pass

#     def test_US04_no_marr(self):
#         dd = {'DIV':'2000-03-01'}
#         self.assertEqual(self.fn(dd), -1)

#     def test_US04_no_div(self):
#         dd = {'MARR':'2000-03-01'}
#         self.assertEqual(self.fn(dd), -1)

#     def test_US04_valid_date(self):
#         dd = {'MARR':'2000-03-01', 'DIV':'2000-03-02'}
#         self.assertEqual(self.fn(dd), 0)

#     def test_US04_valid_date_same(self):
#         dd = {'MARR':'2000-03-01', 'DIV':'2000-03-01'}
#         self.assertEqual(self.fn(dd), 0)

#     def test_US04_invalid_year(self):
#         dd = {'MARR':'2000-03-01', 'DIV':'1999-03-02'}
#         self.assertEqual(self.fn(dd), 1)

#     def test_US04_invalid_day(self):
#         dd = {'MARR':'2000-03-02', 'DIV':'2000-03-01'}
#         self.assertEqual(self.fn(dd), 1)

#     def test_US04_invalid_mon(self):
#         dd = {'MARR':'2000-03-01', 'DIV':'2000-02-02'}
#         self.assertEqual(self.fn(dd), 1)