import inspect
import numpy as np
import string
from random import choice
from random import randint


def n_to_string_of_n_random_uppercase_letters(n=1):
    # n is the number of random uppercase letters

    uppercase_letters = string.ascii_uppercase
    string_of_n_random_uppercase_letters = ''.join(choice(uppercase_letters) for i in range(n))

    return string_of_n_random_uppercase_letters


def n_to_string_of_n_random_lowercase_letters(n=1):
    # n is the number of random lowercase letters

    lowercase_letters = string.ascii_lowercase
    string_of_n_random_lowercase_letters = ''.join(choice(lowercase_letters) for i in range(n))

    return string_of_n_random_lowercase_letters


def n_to_string_of_n_random_digits(n=1):
    # n is the number of random digits

    letters_and_numbers = ''.join([string.ascii_letters, string.digits])
    string_of_n_random_digits = ''.join(choice(letters_and_numbers) for i in range(n))

    return string_of_n_random_digits


def generate_n_random_emails(n=1, range_1=[10, 30], range_2=[5, 15]):
    # n is the number of random emails
    # range_1 is the range of the random m_1 of the e_th email.
    # m_1 is the number of the random digits before "@" of the e_th email.
    # range_2 is the range of the random m_2 of the e_th email.
    # m_2 is the number of the random digits between "@" and ".com" of the e_th email.

    # letters_lowercase = string.ascii_lowercase
    # letters_uppercase = string.ascii_uppercase
    # numbers = string.digits
    # letters = ''.join([letters_lowercase, letters_lowercase])
    # letters_and_numbers = ''.join([string.ascii_letters, string.digits])
    emails = [None] * n
    for e in range(n):

        m_1 = randint(*range_1)
        m_2 = randint(*range_2)

        emails[e] = ''.join([
            n_to_string_of_n_random_digits(n=m_1), '@',
            n_to_string_of_n_random_digits(n=m_2), '.com'])

    return emails


def generate_random_names(n=1, range_m=[5, 10]):
    # n is the number of random names
    # range_m is the range of the random m of the r_th name.
    # m is the number of the random letters of the r_th name.

    names = [None] * n
    for r in range(n):

        m = randint(*range_m)

        names[r] = ''.join([n_to_string_of_n_random_uppercase_letters(n=1),
                            n_to_string_of_n_random_lowercase_letters(n=(m - 1))])

    return names


def get_variable_name(variable, n_outer_frames=1):
    dict_variables = inspect.getouterframes(inspect.currentframe())[n_outer_frames].frame.f_locals
    keys, values = list(dict_variables.keys()), list(dict_variables.values())
    for i, v in enumerate(values):
        try:
            if v == variable:
                name = keys[i]
        except ValueError:
            if (v == variable).all():
                name = keys[i]
    return name


def get_list_of_n_variable_names(variables, n_outer_frames=1):

    n_variables = len(variables)
    list_of_names = [None] * n_variables
    max_string_length = 0
    for i, v in enumerate(variables):
        list_of_names[i] = get_variable_name(v, n_outer_frames=n_outer_frames + 1)
        string_length_i = len(list_of_names[i])
        if string_length_i > max_string_length:
            max_string_length = string_length_i
    return np.asarray(list_of_names, dtype=('<U' + str(max_string_length)))
