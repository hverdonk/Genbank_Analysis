"""create_db.py: Builds an SQLite database from Genbank files.

Command line syntax is as follows:
python3 create_db.py [GENBANK FILES]
"""

__author__ = "Hannah Verdonk"
__copyright__ = "Copyright 2020, Hannah Verdonk"
__license__ = "MIT"
__email__ = "verdonkhannah@gmail.com"

import sys
from Bio import SeqIO
import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Grab all genbank files listed in STDIN
gb_files = sys.argv[1:]

# TODO: if/else statement to handle zipped vs unzipped files, try/catch loops for errors?

# TODO: figure out the correct syntax for doing this, replacing the outer for loop below
# with open genbank.gz as unzipped:
    # parse the unzipped boi

for f in gb_files:
    for seq_record in SeqIO.parse(f, "genbank"):
        pass
        # TODO: find out what fields genbank files have & dump them into the new database

'''
Example code for parsing a genbank file (taken from http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc12)
'''

for seq_record in SeqIO.parse("ls_orchid.gbk", "genbank"):
    print(seq_record.id)
    print(repr(seq_record.seq))
    print(len(seq_record))


'''
This should give:

Z78533.1
Seq('CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGG...CGC', IUPACAmbiguousDNA())
740
...
Z78439.1
Seq('CATTGTTGAGATCACATAATAATTGATCGAGTTAATCTGGAGGATCTGTTTACT...GCC', IUPACAmbiguousDNA())
592


'''




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
