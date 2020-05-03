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
import helper_functions as hf

conn = sqlite3.connect('genbank.db')
c = conn.cursor()

# A genbank ID is accession_number.version_number. Can there be multiple IDs with the same accession number?
# If so, that'll throw off my stats by inflating the number of "unique" records in the system

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS genbank
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

c.execute('''CREATE TABLE IF NOT EXISTS refs
            (ID text, feature_start integer,
            feature_end integer,
            authors text,
            title text,
            journal text,
            comment text);
             ''')

# c.execute('''CREATE TABLE IF NOT EXISTS features
#              (ID text,
#              );
#               '''
#           )


# Grab all genbank files listed in STDIN
gb_files = sys.argv[1:]

for f in gb_files:
    # f = gzip.open(f)  # UNCOMMENT FOR REAL RUN
    for seq_record in SeqIO.parse(f, "genbank"):
        # print(type(seq_record.annotations['references'][0].location[0]))
        # why did I want to check this?
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

        for r in seq_record.annotations['references']:
            if hf.is_compound_location(r.location):
                locations = hf.decompose_compound_location(r.location)
                for loc in locations:
                    entry2 = [(seq_record.id,
                               int(loc.start),
                               int(loc.end),
                               r.authors,
                               r.title,
                               r.journal,
                               r.comment), ]
                    c.executemany('INSERT INTO refs VALUES (?,?,?,?,?,?,?)', entry2)
            else:
                entry2 = [(seq_record.id,
                           int(r.location[0].start),
                           int(r.location[0].end),
                           r.authors,
                           r.title,
                           r.journal,
                           r.comment), ]
                c.executemany('INSERT INTO refs VALUES (?,?,?,?,?,?,?)', entry2)

        lst = []
        for feature in seq_record.features:
            # TODO: add the fields to the table itself
            pass
        #     lst.append(feature)
        # print(lst)
        #    entry3 = [(seq_record.id,
        #               ), ]

# Check that refs table has data in it
c.execute('SELECT * from refs')
print(c.fetchone())

# Save (commit) the changes
conn.commit()

# Close connection after committing changes
conn.close()

"""

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

"""
