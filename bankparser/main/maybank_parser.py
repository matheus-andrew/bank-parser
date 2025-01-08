from enum import Enum
from dataclasses import dataclass
from typing import List
import csv


class Location(Enum):
    JAKARTA_PUSAT = "JAKARTA PUSAT"
    JAKARTA_BARAT = "JAKARTA BARAT"
    JAKARTA_BARA = "JAKARTA BARA"
    JAKARTA_BARA_LOWER = "Jakarta Bara"
    JAKARTA_SELATAN = "JAKARTA SELATAN"
    JAKARTA_SELAT = "JAKARTA SELAT"
    JAKARTA_SLT = "JAKARTA SLT"
    JAKARTA_UTARA = "JAKARTA UTARA"
    TANGERANG = "TANGERANG"
    TANGERANG_K = "Tangerang (K"
    JAKARTA = "JAKARTA"
    MOUNTAIN_VIEW = "MOUNTAIN VIEW"
    JA = "JA"
    UNKNOWN = "-"

    @classmethod
    def get_location(cls, text: str) -> 'Location':
        for location in cls:
            if location.value in text:
                return location
        return cls.UNKNOWN

class Country(Enum):
    INDONESIA = "ID"
    LT = "LT"
    GB = "GB"
    UNKNOWN = "-"

    @classmethod
    def get_country(cls, text: str) -> 'Country':
        for country in cls:
            if country.value in text:
                return country
        return cls.UNKNOWN

@dataclass
class Transaction:
    tanggal_penggunaan: str
    tanggal_cetak: str
    description: str
    location: str
    country: str
    amount: str
    credit: bool

class MaybankParser:
    @staticmethod
    def parse_line(line: str) -> Transaction:
        # Split the first two dates
        dates = line[:17].split()
        tanggal_penggunaan, tanggal_cetak = dates
        line = line[17:].strip()

        # Extract amount and credit status from the end
        credit = line.endswith("CR")
        line = line.rstrip("CR").strip()
        amount_str = line.split()[-1].replace(',', '').replace('.', '')
        amount = float(amount_str)
        formatted_amount = f"{amount:,.0f}"
        line = line[:line.rfind(" ")].strip()

        # Extract country
        country = Country.UNKNOWN.value
        for cou in Country:
            if line.endswith(cou.value):
                country = cou.value
                line = line.replace(cou.value, '').strip()
                break

        # Check for the ":xxx/xxx" pattern and extract it to the 'country' field
        if ":" in line and "/" in line:
            print(line)
            country = line[line.rfind(":") + 1:]
            line = line[:line.rfind(":")].strip()
            print(line)

        # Extract location
        location = Location.UNKNOWN.value
        for loc in Location:
            if loc.value in line:
                location = loc.value
                line = line.replace(loc.value, '').strip()
                break

        # The remaining text is the description
        description = line.strip()

        return Transaction(
            tanggal_penggunaan=tanggal_penggunaan,
            tanggal_cetak=tanggal_cetak,
            description=description,
            location=location,
            country=country,
            amount=formatted_amount,
            credit=credit
        )

    @staticmethod
    def convert_to_csv(input_file: str, output_file: str):
        transactions: List[Transaction] = []
        
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    transaction = MaybankParser.parse_line(line)
                    transactions.append(transaction)

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # Write header
            writer.writerow([
                'tanggal penggunaan',
                'tanggal cetak',
                'description',
                'location',
                'country',
                'amount',
                'credit'
            ])
            
            # Write transactions
            for t in transactions:
                writer.writerow([
                    t.tanggal_penggunaan,
                    t.tanggal_cetak,
                    t.description,
                    t.location.value,
                    t.country.value,
                    t.amount,
                    t.credit
                ])

    @staticmethod
    def parse_text(text: str) -> List[Transaction]:
        transactions = []
        for line in text.split('\n'):
            if line.strip():
                transaction = MaybankParser.parse_line(line)
                transactions.append(transaction)
        return transactions
