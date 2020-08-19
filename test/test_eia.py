import unittest
import eia
import symbols


class TestEIA(unittest.TestCase):

    def test_pull_series(self):
        eia_symbols = [
            'PET.WCRSTUS1.W',
            'PET.WCESTUS1.W',
            'PET.WCSSTUS1.W',
            'PET.WGTSTUS1.W',
        ]
        res = eia.get_symbols(tuple(eia_symbols))
        self.assertEqual(res.loc['2020-01-03']['PET.WCRSTUS1.W'], 1066027.0)

    def test_all_defined_symbols_valid(self):
        res = eia.get_symbols(tuple(symbols.basic.values()))
        for s in symbols.basic.values():
            self.assertIn(s, res.columns)


if __name__ == '__main__':
    unittest.main()


