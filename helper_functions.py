"""helper_functions.py: Functions used to build the code for create_db.py.
"""

__author__ = "Hannah Verdonk"
__copyright__ = "Copyright 2020, Hannah Verdonk"
__license__ = "MIT"
__email__ = "verdonkhannah@gmail.com"

from Bio import SeqIO, SeqFeature


def is_compound_location(loc):
    """
    Returns true if the location object from the Bio.SeqFeature package is a
    compound location object (used to represent features with several parts).
    :param loc: Bio.SeqFeature object
    :return: bool
    """
    if type(loc) is SeqFeature.CompoundLocation:
        return True


def simplify_location(loc):
    """Takes in a compound location. Returns the list of individual
    'Bio.SeqFeature.FeatureLocation' objects that comprised it.
    :param loc:
    :return: bool
    """

