"""create_db.py: Builds an SQLite database from Genbank files.

Command line syntax is as follows:
python3 create_db.py [GENBANK FILES]

Genbank files must be compressed with gzip.
"""

__author__ = "Hannah Verdonk"
__copyright__ = "Copyright 2020, Hannah Verdonk"
__license__ = "MIT"
__email__ = "verdonkhannah@gmail.com"

import sys
from Bio import SeqIO
import gzip
import sqlite3

conn = sqlite3.connect('genbank.db')
c = conn.cursor()

# A genbank ID is accession_number.version_number. Can there be multiple IDs with the same accession number?
# I'm ignoring the database cross-references because I'm not interested in exploring them at the moment.
# Create table
c.execute('''CREATE TABLE genbank
             (ID text,
             accession text,
             name text,
             description text,
             molecule_type text,
             topology text,
             genbank_division text,
             date text,
             source text,
             organism text,
             taxonomy text,
             seq text);
             ''')


# TODO: add these tables
#              CREATE TABLE references
#              ();
#              CREATE TABLE features
#              ()


# Grab all genbank files listed in STDIN
gb_files = sys.argv[1:]

for f in gb_files:
    # f = gzip.open(f)
    for seq_record in SeqIO.parse(f, "genbank"):
        entry = [(seq_record.id,
                  seq_record.annotations['accessions'][0],
                  seq_record.name,
                  seq_record.description,
                  seq_record.annotations['molecule_type'],
                  seq_record.annotations['topology'],
                  seq_record.annotations['data_file_division'],
                  seq_record.annotations['date'],
                  seq_record.annotations['source'],
                  seq_record.annotations['organism'],
                  seq_record.annotations['taxonomy'][-1],
                  str(seq_record.seq)), ]
        c.executemany('INSERT INTO genbank VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', entry)


# Save (commit) the changes
conn.commit()

# Close connection after committing changes
conn.close()

"""Create taxonomy table, link genus in genbank entry to genus in taxonomy table
Each thing in taxonomy list links to previous thing, so you can trace it up a list.

Create a references table linking each reference to its genbank ID

Create a features table linking each genbank id to its features (get features using seq_record.features)

Contents of one genbank entry:

ID: U49845.1
Name: SCU49845
Description: Saccharomyces cerevisiae TCP1-beta gene, partial cds; and Axl2p (AXL2) and Rev7p (REV7) genes, complete cds
Number of features: 9
/molecule_type=DNA
/topology=linear
/data_file_division=PLN
/date=29-OCT-2018
/accessions=['U49845']
/sequence_version=1
/keywords=['']
/source=Saccharomyces cerevisiae (baker's yeast)
/organism=Saccharomyces cerevisiae
/taxonomy=['Eukaryota', 'Fungi', 'Dikarya', 'Ascomycota', 'Saccharomycotina', 'Saccharomycetes', 'Saccharomycetales', 'Saccharomycetaceae', 'Saccharomyces']
/references=[Reference(title='Selection of axial growth sites in yeast requires Axl2p, a novel plasma membrane glycoprotein', ...), Reference(title='Direct Submission', ...)]
Seq('GATCCTCCATATACAACGGTATCTCCACCTCAGGTTTAGATCTCAACAACGGAA...ATC', IUPACAmbiguousDNA())



seq_record.annotations gets you a dictionary with the /keys and their values as a dict. 
References are stored as reference objects. Sequences are stored as sequence objects.


"""

'''
Example code for parsing a genbank file (taken from http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc12)
'''

"""
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




"""
