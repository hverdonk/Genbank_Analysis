"""create_db.py: Builds an SQLite database from Genbank files.

Command line syntax is as follows:
python3 create_db.py [GENBANK FILES]
"""

__author__ = "Hannah Verdonk"
__copyright__ = "Copyright 2020, Hannah Verdonk"
__license__ = "MIT"
__email__ = "verdonkhannah@gmail.com"

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

'''Example Code, taken from https://docs.python.org/3/library/sqlite3.html'''

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
