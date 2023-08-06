"""Function for io operations

In Spring 2020, to demo how to build a Python project, this project was
created for the students in CS4900 senior seminar class. This module contains
the functions about input and output the prime nubmers into or from a csv file.

Example:
    python primeio.py

"""

__author__ = 'Lin Chen'
__version__ = 0.1
__email__ = 'lichen@valdosta.edu'
__status__ = 'Prototype'

import csv

def write_primes(prime_list, file_name):
    """Output a list of prime numbers into a csv file

    Args:
        prime_list (list): a list of prime numbers
        file_name (str): file name of a csv file

    Raises:
        IOError: if file is not able to be opened

    Examples:
        >>> write_primes([2, 3, 5, 7], 'output.csv')

    """
    with open(file_name, 'w') as csvfile:
        writter = csv.writer(csvfile, delimiter=',')
        writter.writerow(prime_list)

def read_primes(file_name):
    """Read a list of prime numbers from a csv file

    Args:
        file_name (str): file name of a csv file

    Raises:
        IOError: if file is not able to be read

    Examples:
        >>> l = read_primes('output.csv')

    """
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            prime_list = []
            for field in row:
                prime_list.append(int(field))
            return prime_list
