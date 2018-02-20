import unittest

class TestUS01(unittest.TestCase):
    def setUp(self):
        from ProcessResult import parse_date
        self.fn = parse_date

    def tearDown(self):
        pass

    def test_US01_well_formed(self):
        date_str = '01 JAN 2018'
        dsc = 'Well-formed date'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == '2018-01-01')
            
    
    def test_US01_well_formed_now(self):
        date_str = '19 FEB 2018'
        dsc = 'Well-formed date: the same date as now'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == '2018-02-19')
        
    def test_US01_ill_formed_year(self):
        date_str = '19 FEB 2100'
        dsc = 'Ill-formed date: YEAR too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')

    def test_US01_ill_formed_day(self):
        date_str = '20 FEB 2018'
        dsc = 'Ill-formed date: DAY too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')
        
    def test_US01_ill_formed_mon(self):
        date_str = '19 MAR 2018'
        dsc = 'Ill-formed date: MONTH too large'
        print('\n' + date_str + ':', dsc)

        self.assertTrue(self.fn(date_str) == 'INVALID_DATE')



class TestUS04(unittest.TestCase):
    def setUp(self):
        from ProcessResult import check_marrdiv_date
        self.fn = check_marrdiv_date

    def tearDown(self):
        pass

    def test_US04_no_marr(self):
        dd = {'DIV':'2000-03-01'}
        self.assertEqual(self.fn(dd), -1)

    def test_US04_no_div(self):
        dd = {'MARR':'2000-03-01'}
        self.assertEqual(self.fn(dd), -1)

    def test_US04_valid_date(self):
        dd = {'MARR':'2000-03-01', 'DIV':'2000-03-02'}
        self.assertEqual(self.fn(dd), 0)

    def test_US04_valid_date_same(self):
        dd = {'MARR':'2000-03-01', 'DIV':'2000-03-01'}
        self.assertEqual(self.fn(dd), 0)

    def test_US04_invalid_year(self):
        dd = {'MARR':'2000-03-01', 'DIV':'1999-03-02'}
        self.assertEqual(self.fn(dd), 1)

    def test_US04_invalid_day(self):
        dd = {'MARR':'2000-03-02', 'DIV':'2000-03-01'}
        self.assertEqual(self.fn(dd), 1)

    def test_US04_invalid_mon(self):
        dd = {'MARR':'2000-03-01', 'DIV':'2000-02-02'}
        self.assertEqual(self.fn(dd), 1)