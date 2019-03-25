
import sys
from xlrd import open_workbook
from decimal import Decimal, InvalidOperation
import tempfile 

def convert(file):
    temp = tempfile.SpooledTemporaryFile(mode='w+t') 
    book = open_workbook(file)
    s = book.sheet_by_index(0)
    col_search = True
    amount_col = -1
    transaction_date_col = -1
    details_col = -1
    transactions = []
    for row in range(s.nrows):
        # we are searching for column identifiers
        if col_search:
            for col in range(s.ncols):
                contents = s.cell(row, col).value
                if contents == "Amount":
                    amount_col = col
                    col_search = False # done searching
                elif contents == "Transaction Date":
                    transaction_date_col = col
                elif contents == "Details":
                    details_col = col
        else:
            try:
                amount = s.cell(row, amount_col).value.split("\n")[0]
                transaction_date = s.cell(row, transaction_date_col).value.split("\n")[0]
                details = s.cell(row, details_col).value.split("\n")[0]
                Decimal(amount)
                transactions.append((transaction_date, amount, details))
            except InvalidOperation:
                pass
    try:
        temp.write(b"!Type:Bank\n")
        for t in transactions:
            temp.write(b"D" + t[0] + "\n")
            temp.write(b"T" + t[1] + "\n")
            temp.write(b"P" + t[2] + "\n")
            temp.write(b"^" + "\n")
    finally:
        final = BytesIO(temp.read())
        temp.close()
