from django.test import TestCase

from main.bca_parser import BCAParser
from main.maybank_parser import MaybankParser


# Create your tests here.
class TestBCAParser(TestCase):
    def setUp(self):
        self.parser = BCAParser()

    def test_parse_valid_data(self):
        # Replace with actual input and expected result
        sample_data = "28-NOV 04-DES KOR BIAYA IURAN TAHUNAN 125.000 CR"
        parsed_result = self.parser.parse_line(sample_data)

        # Replace with the expected structure
        expected_result = {
            "transaction_date": "28-NOV",
            "posting_date": "04-DES",
            "description": "KOR BIAYA IURAN TAHUNAN",
            "amount": "125,000",
            "is_credit": True,
        }

        self.assertEqual(parsed_result.__dict__, expected_result)

    def test_parse_invalid_data(self):
        sample_data = "INVALID DATA FORMAT"
        with self.assertRaises(ValueError):  # Replace ValueError with the specific exception you expect
            self.parser.parse_line(sample_data)


class TestMaybankParser(TestCase):
    def setUp(self):
        self.parser = MaybankParser()

    def test_parse_valid_data(self):
        # Replace with actual input and expected result
        sample_data = "02-12-24 03-12-24 Grab* A-77CEEF3GWGOR JAKARTA PUSATID 51.900"
        parsed_result = self.parser.parse_line(sample_data)

        # Replace with the expected structure
        expected_result = {
            "tanggal_penggunaan": "02-12-24",
            "tanggal_cetak": "03-12-24",
            "description": "Grab* A-77CEEF3GWGOR",
            "location": "JAKARTA PUSAT",
            "country": "ID",
            "amount": "51,900",
            "credit": False,
        }

        self.assertEqual(parsed_result.__dict__, expected_result)

    def test_parse_invalid_data(self):
        sample_data = "INVALID DATA FORMAT"
        with self.assertRaises(ValueError):  # Replace ValueError with the specific exception you expect
            self.parser.parse_line(sample_data)
