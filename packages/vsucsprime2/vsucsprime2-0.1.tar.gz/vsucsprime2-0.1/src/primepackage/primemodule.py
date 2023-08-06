"""Functions for prime numbers

In Spring 2020, to demo how to build a Python project, this project was
created for the students in CS4900 senior seminar class. This module contains
the functions about prime numbers.

Example:
    python primemodule.py

"""

__author__ = "Lin Chen"
__version__ = 0.1
__email__ = "lichen@valdosta.edu"
__status__ = "Prototype"

def is_prime(number):
    """Check if a number is a prime

    Args:
        number (int): integer number

    Return:
        boolean: true if n is a prime number, false otherwise

    Raises:
        ValueError: if n is not a natural number

    Examples:
        >>> b = is_prime(83)

    """
    if not isinstance(number, int):
        raise ValueError("Not an integer number")

    if number <= 0:
        raise ValueError("Not a natural number")

    if number == 1:
        return False

    for i in range(2, number):
        if number%i == 0:
            return False

    return True

def get_n_prime(num):
    """Get the fist num prime numbers

    Args:
        num (int): the number of the first prime numbers

    Return:
        list: a list of integer numbers

    Examples:
        >>> prime_list = get_n_prime(10)

    """
    current_num = 2
    count = 0
    prime_list = []

    while True:
        if is_prime(current_num):
            prime_list.append(current_num)
            count += 1
            if count == num:
                return prime_list
        current_num += 1
