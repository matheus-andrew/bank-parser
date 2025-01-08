from enum import Enum
from dataclasses import dataclass
from typing import List
import csv
import re
from datetime import datetime

@dataclass
class Transaction:
    transaction_date: str
    posting_date: str
    description: str
    amount: str
    is_credit: bool

class BCAParser:
    MONTHS = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
        'MEI': '05', 'JUN': '06', 'JUL': '07', 'AGU': '08',
        'SEP': '09', 'OKT': '10', 'NOV': '11', 'DES': '12'
    }

    @staticmethod
    def convert_date(date_str: str) -> str:
        """Convert date from DD-MMM format to DD-MM format"""
        day, month = date_str.split('-')
        return f"{day.zfill(2)}-{BCAParser.MONTHS[month]}"

    @staticmethod
    def parse_line(line: str) -> Transaction:
        # Split the first two dates
        parts = line.strip().split()
        transaction_date = parts[0]
        posting_date = parts[1]

        # Check if the line ends with CR
        is_credit = line.strip().endswith('CR')

        # Extract amount (last number in the line)
        amount_str = ''
        for part in reversed(parts):
            if part == 'CR':
                continue
            try:
                amount_str = part.replace('.', '').replace(',', '')
                float(amount_str)  # Verify it's a valid number
                break
            except ValueError:
                continue

        amount = float(amount_str)
        formatted_amount = f"{amount:,.0f}"

        # Extract description (everything between dates and amount)
        description_parts = parts[2:-1] if not is_credit else parts[2:-2]
        description = ' '.join(description_parts)

        return Transaction(
            transaction_date=transaction_date,
            posting_date=posting_date,
            description=description,
            amount=formatted_amount,
            is_credit=is_credit
        )

    @staticmethod
    def convert_to_csv(input_file: str, output_file: str):
        transactions: List[Transaction] = []
        
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    transaction = BCAParser.parse_line(line)
                    transactions.append(transaction)

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # Write header
            writer.writerow([
                'transaction_date',
                'posting_date',
                'description',
                'amount',
                'is_credit'
            ])
            
            # Write transactions
            for t in transactions:
                writer.writerow([
                    t.transaction_date,
                    t.posting_date,
                    t.description,
                    t.amount,
                    t.is_credit
                ])
