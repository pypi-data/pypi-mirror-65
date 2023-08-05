# default libraries
import unicodedata
import sys
from functools import wraps
from math import log
from collections import Counter



def cached_property(prop):
    """ Property that will replace itself with a calculated value """
    name = '__' + prop.__name__

    @wraps(prop)
    def wrapper(self):
        if not hasattr(self, name):
            setattr(self, name, prop(self))
        return getattr(self, name)
    return property(wrapper)


class TextStats(object):
    """ Performs statiscal calculation on input text """


    def __init__(self, input_text):
        self.input_text = input_text

    @cached_property
    def length(self):
        """ Gets input text length

        Return type: int
        """
        return len(self.input_text)

    @cached_property
    def alphabet(self):
        """ Gets a distinct list of alphabets

        Return type: set

        """
        return set(self.input_text)

    @cached_property
    def alphabet_cardinal(self):
        """ Gets the alphabet cardinals

        Return type: int
        """
        return len(self.input_text)

    @cached_property
    def char_categories_detailed(self):
        """ Character count per unicode category, detailed format.
        refer: http://www.unicode.org/reports/tr44/#GC_Values_Table

        Return type: collections.Counter
        """
        return Counter(map(unicodedata.category, self.input_text))

    @cached_property
    def char_categories(self):
        """ Character count per character category

        The following categories are:

        # L: letter
        # M: Mark
        # N: Number
        # P: Punctuation
        # S: Symbol
        # Z: Separator
        # C: Othereturn: Counter(unicode-character-category: count }

        Return type: collections.Counter
        """
        c = Counter()
        for cat, n in self.char_categories_detailed.items():
            c[cat[0]] += n
        return c

    @cached_property
    def letters(self):
        """ Count all letters

        Return type: int
        """
        return self.char_categories['L']

    @cached_property
    def letters_lowercase(self):
        """ Count lowercase letters

        Return type: int
        """
        return self.char_categories_detailed['Ll']

    @cached_property
    def letters_uppercase(self):
        """ Count uppercase letters

        Return type: int
        """
        return self.char_categories_detailed['Lu']

    @cached_property
    def numbers(self):
        """ Count numbers

        Return type: int
        """
        return self.char_categories['N']

    @cached_property
    def special_characters(self):
        """ Count special characters

        Return type: int
        """
        return self.count_except('L', 'N')

    @cached_property
    def non_letter(self):
        """ Count non letter characters

        Return type: int
        """
        return self.numbers + self.special_characters

    @cached_property
    def entropy_bits(self):
        """ Get information entropy bits: log2 of the number of possible passwords
        https://en.wikipedia.org/wiki/Password_strength

        Return type:rtype: float
        """
        return self.length * log(self.alphabet_cardinal, 2)

    @cached_property
    def entropy_density(self):
        """ Get information entropy density factor, ranged {0 .. 1}.
        If all provided characters are unique then the max value is 1
        Return type: float
        """
        return log(self.alphabet_cardinal, self.length)

    def count(self, *categories):
        """ Count characters for the specified class categories
        Return type: int
        """
        return sum([int(cat_n[0] in categories) * cat_n[1] for cat_n in list(self.char_categories.items())])

    def count_except(self, *categories):
        """ Count characters of all classes apart from the ones provided
        Return type: int
        """
        return sum([int(cat_n1[0] not in categories) * cat_n1[1] for cat_n1 in list(self.char_categories.items())])

    def strength(self, min_bits=30):
        """ Get password strength as a number normalized to range {0 .. 1}.

        https://en.wikipedia.org/wiki/Password_strength

        WEAK < 0.33
        MEDIUM > 0.33 and < 0.66
        STRONG > 0.66

        Return type: float
        """
        WEAK_MAX = 0.334

        if self.entropy_bits <= min_bits:
            return WEAK_MAX * self.entropy_bits / min_bits

        HARD_BITS = min_bits * 3
        HARD_VALUE = 0.950

        k = -log((1 - HARD_VALUE) / (1-WEAK_MAX), 2) / HARD_BITS
        f = lambda x: 1 - (1-WEAK_MAX)*pow(2, -k*x)

        return f(self.entropy_bits - min_bits)
