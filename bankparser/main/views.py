from django.shortcuts import render
from main.maybank_parser import MaybankParser
from main.bca_parser import BCAParser
import io

def index(request):
    context = {
        'input_data': '',
        'transactions': None,
        'error_message': None,
        'parser_type': 'maybank'  # default parser
    }

    if request.method == 'POST':
        transaction_data = request.POST.get('transaction_data', '').strip()
        parser_type = request.POST.get('parser_type', 'maybank')
        
        context['input_data'] = transaction_data
        context['parser_type'] = parser_type

        if transaction_data:
            try:
                # Create a string buffer to write the data
                input_buffer = io.StringIO(transaction_data)
                transactions = []
                
                # Parse each line based on selected parser
                for line in input_buffer:
                    if line.strip():
                        if parser_type == 'maybank':
                            transaction = MaybankParser.parse_line(line)
                        else:
                            transaction = BCAParser.parse_line(line)
                        transactions.append(transaction)
                
                context['transactions'] = transactions
            except Exception as e:
                context['error_message'] = f"Error parsing data: {str(e)}"
        else:
            context['error_message'] = "Please enter some transaction data."

    return render(request, 'index.html', context)