import unittest

class TestUC01(unittest.TestCase):
    def setUp(self):
        from ProcessResult import parse_date
        self.fn = parse_date

    def tearDown(self):
        pass

    def test_UC01_well_formed(self):
        date_str = '01 JAN 2018'
        dsc = 'Well-formed date'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == '2018-01-01')
            
    
    def test_UC01_well_formed_now(self):
        date_str = '19 FEB 2018'
        dsc = 'Well-formed date: the same date as now'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == '2018-02-19')
        
    def test_UC01_ill_formed_year(self):
        date_str = '19 FEB 2100'
        dsc = 'Ill-formed date: YEAR too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')

    def test_UC01_ill_formed_day(self):
        date_str = '20 FEB 2018'
        dsc = 'Ill-formed date: DAY too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')
        
    def test_UC01_ill_formed_mon(self):
        date_str = '19 MAR 2018'
        dsc = 'Ill-formed date: MONTH too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')