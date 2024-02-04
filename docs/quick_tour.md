# Quick tour

Let's start with a simple example. We will create a simple application.

Use case:
- We have a bookstore.
- Every day, our warehouse exports CSV files with actual stock.
- We want to write an app to manage selling.
- After-sell invoices should be stored in the system.
- At the end of the day, we should be able to print all invoices for a given day.

An example will be written with trivial code, without frameworks, to show how to use RedBeanPython.

At the end of this tutorial, you will find a complete example code that you can copy and run.

## Loading data

First, install RedBeanPython:

```bash
pip install redbeanpython
```

The CSV file `warehouse.csv` that our warehouse exports every day has a structure like this:

```csv
Title,ISBN,Price,Quantity
"Dune","9780441013593",12.99,8
"Ender's Game","9780812550702",7.99,0
"The Hitchhiker's Guide to the Galaxy","9780345391803",6.99,20
"Neuromancer","9780441569595",8.99,12
(...)
```

Let's import it to the database:

```python
from decimal import Decimal

from redbeanpython import Bean, r

#We will use the SQLite database stored in the current directory
r.setup(dsn="sqlite:///test.sqlite")

with open('warehouse.csv', newline='') as csvfile:
    for row in csv.DictReader(csvfile):
        # create new bean
        book = Bean('book')
        # and fill it with data from the CSV
        book.id = row['ISBN']
        book.title = row['Title']
        # We will use Decimal type for the price
        book.price = Decimal(row['Price'])
        book.quantity = int(row['Quantity'])
        # and that's all, store it
        r.store(book)
```

When we run this code, we store all books from the CSV file in a database. Nothing else is needed.

Now we can start selling books.

```python
from datetime import date

from redbeanpython import NotExistsError

# We want to create an invoice for every book we sell
invoice = Bean('invoice')

# As invoices have to be enumerated consistently, we have to find the  last invoice number
invoice_id = 0

if r.count('invoice') != 0:
    # If there are any invoices in the database,
    # we will find the last one
    # and use its id as the previous number
    last_invoice = list(r.find('invoice', order='id DESC', limit=1))[0]
    invoice_id = int(last_invoice.id) + 1

invoice.id = str(invoice_id)

invoice.customer = input('What is the customer name?\n')
invoice.issue_date = date.today()
invoice.total = Decimal('0.0')

while True:
    isbn = input('What is the ISBN of the book you want to sell?\n')
    try:
        # We will try to load the book from the database
        book = r.load('book', isbn, throw_on_empty=True)

        # And check if it is in stock
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
        print('Chose one of the following:')
        for book in r.find('book'):
            print(f'- {book.title}')

print(f'Your invoice number: {invoice.id}')

```

If we rerun this code, we observe that the database structure was extended. 

Now lets print all invoices for the given day:

```python
invoice_date = input('What is the date of the invoices you want to print? (YYYY-MM-DD)\n')
invoice_date = date.fromisoformat(invoice_date)
for invoice in r.find('invoice', query="issue_date = :date", params={'date': invoice_date}):
    print(f'Invoice {invoice.id} for {invoice.customer} with total {invoice.total:.2f}')
    book = r.load("book", invoice.book_id)
    print(f'  Book: {book.title}')
```

Finally, we would need some stats of our business:

```python
invoices_total = r.count('invoice')
print(f"Total invoices: {invoices_total}")
out_of_stock = r.find('book', query="quantity = 0")
print(f"Out-of-stock books:")
for book in out_of_stock:
    print(f"- {book.title} {book.id}")
```

And that's all. We have a simple application to manage our bookstore.

Let's check how it works:

```bash
  Generating migrations/versions/1706778405406427_.py # (1)
What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")
  sell_books
What is the customer name?
  Adam
What is the ISBN of the book you want to sell?
  9780441013593
  Generating migrations/versions/1706778427235189_.py ...  done # (2)
Your invoice number: 1

What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")
  sell_books
What is the customer name?
  Ivona
What is the ISBN of the book you want to sell?
  9780812550702
Sorry, we are out of stock.

What is the ISBN of the book you want to sell?
  1234
Sorry, we do not have that book.

Chose one of:
- Dune 9780441013593
- Ender's Game 9780812550702
- The Hitchhiker's Guide to the Galaxy 9780345391803
- Neuromancer 9780441569595

What is the ISBN of the book you want to sell?
  9780441569595
Your invoice number: 2

What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")
  print_invoices
What is the date of the invoices you want to print? (YYYY-MM-DD)
  2024-02-01
Invoice 1 for Adam with total 12.99
  Book: Dune
Invoice 2 for Ivona with total 8.99
  Book: Neuromancer

What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")
  show_stats
Total invoices: 2
Out of stock books:
- Ender's Game 9780812550702

What do you want to do? ("sell_books", "print_invoices", "show_stats", "exit")
  exit
Bye!
```

1. Migration has been generated in the background as we load books for the first time.
2. We are adding an invoice to the database for the first time, so migration has been generated in the background.

## Full code

If you want to check yourselves, install RedBeanPython, copy, and run this code.

```python
#!/usr/bin/env python3
# coding: utf-8

import csv
from datetime import date
from decimal import Decimal

from redbeanpython import Bean, r, NotExistsError

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
                    print('Chose one of the following:')
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
            print(f"Out-of-stock books:")
            for book in out_of_stock:
                print(f'- {book.title} {book.id}')
        case 'exit':
            print('Bye!')
            exit(0)
        case _:
            print('Sorry, I did not understand that command.')
```

#
# ___