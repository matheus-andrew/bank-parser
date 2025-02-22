from dataclasses import dataclass
from typing import List

@dataclass
class Transaction:
    tgl_transaksi: str
    tgl_pembukuan: str
    keterangan: str
    transaksi_valas: str
    nilai_tukar: str
    jumlah: str
    is_credit: bool

class BRIParser:
    @staticmethod
    def parse_line(line: str) -> Transaction:
        """
        Parse a single line of BRI bank statement
        Format: tanggal transaksi; tanggal pembukuan; keterangan; transaksi valas; nilai tukar; jumlah
        """
        parts = line.strip().split(' ')

        # Get transaction date and posting date (first two elements)
        tgl_transaksi = parts[0]
        tgl_pembukuan = parts[1]

        # Check if the last part ends with CR and get amount
        is_credit = parts[-1].endswith('CR')
        amount_str = parts[-1].replace('CR', '') if is_credit else parts[-1]
        amount = amount_str.replace('.', '')  # Remove thousand separator
        amount = float(amount.replace(',', '.'))  # Convert to float
        formatted_amount = f"{amount:,.0f}"

        # Check if line has currency and exchange rate (counting from the amount backwards)
        if len(parts) >= 7 and parts[-4] == 'IDR':  # Changed from 8 to 7
            transaksi_valas = parts[-4]  # IDR is 4th from last
            nilai_tukar = f"{parts[-3]} {parts[-2]}"  # 0.00 0.00 are 3rd and 2nd from last
            keterangan = ' '.join(parts[2:-4])  # Exclude IDR and exchange rates from description
        else:
            transaksi_valas = '-'
            nilai_tukar = '-'
            keterangan = ' '.join(parts[2:-1])  # Everything between dates and amount
        
        return Transaction(
            tgl_transaksi=tgl_transaksi,
            tgl_pembukuan=tgl_pembukuan,
            keterangan=keterangan,
            transaksi_valas=transaksi_valas,
            nilai_tukar=nilai_tukar,
            jumlah=formatted_amount,
            is_credit=is_credit
        )

    @staticmethod
    def parse_text(text: str) -> List[Transaction]:
        """Parse multiple lines of BRI bank statement text"""
        transactions = []
        lines = text.strip().split('\n')
        
        for line in lines:
            if line.strip():
                transaction = BRIParser.parse_line(line)
                transactions.append(transaction)
        
        return transactions 