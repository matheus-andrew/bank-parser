from django.test import TestCase

from main.bca_parser import BCAParser
from main.maybank_parser import MaybankParser
from main.bri_parser import BRIParser


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


class TestBRIParser(TestCase):
    def setUp(self):
        self.parser = BRIParser()

    def test_parse_line(self):
        test_line = "20-01-2025 21-01-2025 05-BIAYA NOTIFIKASI 01/25 IDR 0.00 0.00 7.500"
        
        result = self.parser.parse_line(test_line)
        
        self.assertEqual(result.tgl_transaksi, '20-01-2025')
        self.assertEqual(result.tgl_pembukuan, '21-01-2025')
        self.assertEqual(result.keterangan, '05-BIAYA NOTIFIKASI 01/25')
        self.assertEqual(result.transaksi_valas, 'IDR')
        self.assertEqual(result.nilai_tukar, '0.00 0.00')
        self.assertEqual(result.jumlah, '7,500')
        self.assertFalse(result.is_credit)

    def test_parse_credit_amount(self):
        test_line = "05-02-2025 05-02-2025 PAYMENT_BERSAMA_00000000000000133724 IDR 0.00 0.00 200.000CR"
        
        result = self.parser.parse_line(test_line)
        
        self.assertEqual(result.tgl_transaksi, '05-02-2025')
        self.assertEqual(result.tgl_pembukuan, '05-02-2025')
        self.assertEqual(result.keterangan, 'PAYMENT_BERSAMA_00000000000000133724')
        self.assertEqual(result.transaksi_valas, 'IDR')
        self.assertEqual(result.nilai_tukar, '0.00 0.00')
        self.assertEqual(result.jumlah, '200,000')
        self.assertTrue(result.is_credit)

    def test_parse_text(self):
        test_data = """20-01-2025 21-01-2025 05-BIAYA NOTIFIKASI 01/25 IDR 0.00 0.00 7.500
05-02-2025 05-02-2025 PAYMENT_BERSAMA_00000000000000133724 IDR 0.00 0.00 200.000CR"""
        
        results = self.parser.parse_text(test_data)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].jumlah, '7,500')
        self.assertFalse(results[0].is_credit)
        self.assertEqual(results[1].jumlah, '200,000')
        self.assertTrue(results[1].is_credit)

    def test_parse_line_without_currency(self):
        test_line = "20-02-2025 20-02-2025 TOTAL INTEREST & SERVICE CHARGE 25.230"
        
        result = self.parser.parse_line(test_line)
        
        self.assertEqual(result.tgl_transaksi, '20-02-2025')
        self.assertEqual(result.tgl_pembukuan, '20-02-2025')
        self.assertEqual(result.keterangan, 'TOTAL INTEREST & SERVICE CHARGE')
        self.assertEqual(result.transaksi_valas, '-')
        self.assertEqual(result.nilai_tukar, '-')
        self.assertEqual(result.jumlah, '25,230')
        self.assertFalse(result.is_credit)
