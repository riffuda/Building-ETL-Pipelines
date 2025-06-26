import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import scrape_page

class TestScrapePage(unittest.TestCase):
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    REQUIRED_KEYS = {"title", "price", "rating", "colors", "size", "gender"}

    def setUp(self):
        self.results = scrape_page(self.BASE_URL)

    def test_data_is_not_empty(self):
        self.assertGreater(len(self.results), 0, "Expected non-empty result from scraper.")

    def test_data_format(self):
        self.assertIsInstance(self.results, list, "Scraped data should be a list.")
        self.assertIsInstance(self.results[0], dict, "Each entry should be a dictionary.")

    def test_required_fields_exist(self):
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, self.results[0], f"Missing required field: '{key}'")

if __name__ == "__main__":
    unittest.main()
