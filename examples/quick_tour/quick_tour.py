#!/usr/bin/env python3
# coding: utf-8

import csv
from datetime import date
from decimal import Decimal

from redbeanpython import Bean
from redbeanpython import NotExistsError
from redbeanpython import r

r.setup(dsn="sqlite:///test.sqlite")

# Create some test data to play with
with open('warehouse.csv', 'w') as f:
    f.write("""Title,ISBN,Price,Quantity
"Dune","1",12.99,8
"Ender's Game","2",7.99,0
"The Hitchhiker's Guide to the Galaxy","3",6.99,20
"Neuromancer","4",8.99,12""")

with open('warehouse.csv', newline='') as csvfile:
    for row in csv.DictReader(csvfile):
        book = Bean('book')
        book.id = row['ISBN']
        book.title = row['Title']
        book.price = Decimal(row['Price'])
        book.quantity = int(row['Quantity'])
        r.store(book)

while True:
    match input('What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")\n'):
        case 'sell_books':
            invoice = Bean('invoice')
            invoice_id = 1
            if r.count('invoice') != 0:
                last_invoice = list(r.find('invoice', order='id DESC', limit=1))[0]
                invoice_id = int(last_invoice.id) + 1
            invoice.id = str(invoice_id)
            invoice.issue_date = date.today()
            invoice.customer = input('What is the customer name?\n')
            invoice.total = Decimal('0.0')

            while True:
                isbn = input('What is the ISBN of the book you want to sell?\n')
                try:
                    book = r.load('book', isbn, throw_on_empty=True)
                    if book.quantity > 0:
                        book.quantity -= 1
                        r.store(book)
                        invoice.total += book.price
                        invoice.book_id = book.id
                        r.store(invoice)
                        break
                    else:
                        print('Sorry, we are out of stock.\n')
                except NotExistsError:
                    print('Sorry, we do not have that book.\n')
                    print('Chose one of:')
                    for book in r.find('book'):
                        print(f'- {book.title} {book.id}')

            print(f'Your invoice number: {invoice.id}')

        case 'print_invoices':
            invoice_date = input('What is the date of the invoices you want to print? (YYYY-MM-DD)\n')
            try:
                invoice_date = date.fromisoformat(invoice_date)
            except ValueError:
                print('Sorry, I did not understand that format.')
                break
            for invoice in r.find('invoice', query="issue_date = :date", params={'date': invoice_date}):
                print(f'Invoice {invoice.id} for {invoice.customer} with total {invoice.total:.2f}')
                book = r.load("book", invoice.book_id)
                print(f'  Book: {book.title}')

        case 'show_stats':
            invoices_total = r.count('invoice')
            print(f"Total invoices: {invoices_total}")
            out_of_stock = r.find('book', query="quantity = 0")
            print(f"Out of stock books:")
            for book in out_of_stock:
                print(f"- {book.title} {book.id}")
        case 'exit':
            print('Bye!')
            exit(0)
        case _:
            print('Sorry, I did not understand that command.')
