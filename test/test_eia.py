import unittest

from eia_weekly_oil_dash import weeklypetreport


class TestEIA(unittest.TestCase):

    def test_generate_page(self):
        res = weeklypetreport.gen_page(title='DOE Weekly Quick Report', template=r'..\eia_weekly_oil_dash\templates\doe_weekly_summary.html',
                                       out_loc=r'..\dist\index.html')
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
