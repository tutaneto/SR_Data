import unittest
from datetime import datetime as dt, timedelta
from libraries.get_prices import get_prices, download_data_all
from libraries.indexes import bc_sgs_get_index_values, ibge_get_index_values
from libraries.gvar import gvar

class TestFinancialData(unittest.TestCase):
    def setUp(self):
        # Initialize test environment
        gvar['ONLINE'] = True
        gvar['ERROR_STATE'] = 0
        self.test_symbols = '^BVSP,^DJI,BRL=X'  # Test with Bovespa, Dow Jones, and BRL/USD
        self.bcb_test_code = '432'  # SELIC daily rate
        self.ibge_test_code = 'INPC'  # National Consumer Price Index

    def tearDown(self):
        # Reset error state after each test
        gvar['ERROR_STATE'] = 0

    def test_bulk_market_data(self):
        """Test bulk market data download"""
        data = download_data_all(self.test_symbols)
        self.assertIsNotNone(data)
        self.assertEqual(gvar['ERROR_STATE'], 0, "Error occurred during bulk data download")

        # Verify data structure
        self.assertIsInstance(data, dict)
        test_symbols = self.test_symbols.split(',')
        for symbol in test_symbols:
            self.assertIn(symbol, data)
            symbol_data = data[symbol]
            self.assertIn('regularMarketPrice', symbol_data)
            self.assertIn('regularMarketPreviousClose', symbol_data)
            # Verify at least previous close is available (even when market is closed)
            self.assertGreater(symbol_data['regularMarketPreviousClose'], 0)

    def test_individual_prices(self):
        """Test individual symbol price fetching"""
        test_symbols = ['^BVSP', 'BRL=X', '^DJI']
        for symbol in test_symbols:
            market_price, close_price = get_prices(symbol)
            self.assertEqual(gvar['ERROR_STATE'], 0, f"Error fetching prices for {symbol}")
            self.assertIsInstance(market_price, (int, float))
            self.assertIsInstance(close_price, (int, float))
            # Market might be closed (price = 0), but previous close should exist
            self.assertGreaterEqual(market_price, 0)
            self.assertGreater(close_price, 0)

    def test_bcb_sgs_data(self):
        """Test Brazilian Central Bank SGS data collection"""
        data = bc_sgs_get_index_values(self.bcb_test_code)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

        # Verify data structure
        self.assertIn('data', data.columns)
        self.assertIn('valor', data.columns)
        self.assertTrue(data['valor'].dtype in ['float64', 'int64'])

    def test_ibge_data(self):
        """Test IBGE data collection"""
        data = ibge_get_index_values(self.ibge_test_code)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

        # Verify data structure
        self.assertIn('data', data.columns)
        self.assertIn('valor', data.columns)
        self.assertTrue(data['valor'].dtype in ['float64', 'int64'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
