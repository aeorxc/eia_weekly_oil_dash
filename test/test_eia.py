import unittest
import eia


class TestEIA(unittest.TestCase):

    def test_pull_series(self):
        eia_symbols = [
            'PET.WCRSTUS1.W',
            'PET.WCESTUS1.W',
            'PET.WCSSTUS1.W',
            'PET.WGTSTUS1.W',
        ]
        res = eia.symbols(tuple(eia_symbols))
        self.assertEqual(res.loc['2020-01-03']['PET.WCRSTUS1.W'], 1066027.0)




if __name__ == '__main__':
    unittest.main()


