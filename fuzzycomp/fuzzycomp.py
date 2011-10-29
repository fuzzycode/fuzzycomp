# Copyright (C) 2011  Bjoern Larsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#TODO: Write up the documentation for all functions

from exceptions import IndexError, ValueError
from math import floor
import itertools
import re

__all__ = ["levenshtein_distance", "jaccard_distance", "soerensen_index", "hamming_distance",
           "lcs_length", "jaro_distance", "jaro_winkler", "dice_coefficient", "soundex", "nysiis" ]

class Matrix(object):
    def __init__(self, rows, cols, default = 0):
        if rows < 0 or cols < 0:
            raise ValueError("Array size must not be negative.")

        self.rows = rows
        self.cols = cols
        self.data = [[default for _ in range(cols)] for _ in range(rows)]

    def __setitem__(self,pos, v):
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            self.data[pos[0]][pos[1]] = v
        else:
            raise IndexError( "Index out of bounds ( %d, %d )" %( pos[0], pos[1] ) )

    def __getitem__(self, pos):
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            return self.data[pos[0]][pos[1]]
        else:
            raise IndexError( "Index out of bounds ( %d, %d )" %( pos[0], pos[1] ) )

    def __str__(self):
        return '\n'.join(['Row %s = %s' % (i, self.data[i]) for i in range(self.rows)])

    def __repr__(self):
        return 'Matrix(%d, %d)' % (self.rows, self.cols)

    def size(self):
        return self.rows, self.cols

def levenshtein_distance( lhs, rhs ):
    """
    Calculates the Levenshtein distance between two strings.
    The comparison is case sensitive.

    See Wikipedia_ for more info on the Levenshtein distance.
    .. _Wikipedia : https://secure.wikimedia.org/wikipedia/en/wiki/Levenshtein_distance

    :param lhs: First string
    :param rhs: Second string
    :return: An integer representing the distance between the strings. The lower value the better
     match. 0 indicates a perfect match.
    :raise: ValueError if any of the strings is empty.
    """

    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")
    

    m = Matrix( len(lhs), len(rhs) )

    for i in range( len( lhs ) ):
        m[ i, 0 ] =  i
    for i in range( len(rhs) ):
        m[ 0, i ] =  i


    for j in range( 1, len(rhs) ):
        for i in range( 1, len( lhs ) ):
            if lhs[ i ] == rhs[ j ]:
                m[ i, j ] = m[ i - 1, j - 1 ]
            else:
                m[ i, j ] = min( m[ i - 1, j ] + 1 , m[ i, j - 1 ] + 1, m[ i - 1, j - 1] + 1 )


    return m[ len(lhs) - 1, len(rhs) - 1 ]

def jaccard_distance( lhs, rhs ):
    """
    Calculates the Jaccard Distance.
    See https://secure.wikimedia.org/wikipedia/en/wiki/Jaccard_index for details

    :param lhs: First string to match
    :param rhs: Second string to match
    :return: A float in the range [ 0.0, 1.0 ]. 0.0 indicates a perfect match
    """

    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")

    s1 = set( lhs )
    s2 = set( rhs )

    try:
        return  1 - float(len(s1.intersection( s2 ))) / float(len(s1.union( s2 )))
    except ZeroDivisionError:
        return 1

def soerensen_index( lhs, rhs ):
    """
    https://secure.wikimedia.org/wikipedia/en/wiki/S%C3%B8rensen_similarity_index

    :param lhs:
    :param rhs:
    :return: A value in the range [0.0 , 1.0]. 1.0 Indicates a perfect match
    """

    if not lhs or not rhs: raise ValueError("Input can not be empty")
    if type(lhs) != type(rhs): raise ValueError( "Input should be of the same type" )

    common = [ item for item in lhs if item in rhs ]
    return ( 2 * len( common ) ) / float(( len(lhs) + len(rhs) ))

def hamming_distance(lhs, rhs):
    """
    https://secure.wikimedia.org/wikipedia/en/wiki/Hamming_distance
    
    :param lhs:
    :param rhs:
    :return:
    :raise: Value Error if both iterables are not equal length
    """
    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")

    if len(lhs) == len(rhs):
        return sum(ch1 != ch2 for ch1, ch2 in zip(lhs, rhs))
    else:
        raise ValueError("Iterables should be equal length")


def lcs_length(lhs, rhs):
    """
    Calculates the longest common subsequence.

    https://secure.wikimedia.org/wikipedia/en/wiki/Longest_common_subsequence_problem
    
    :param lhs:
    :param rhs:
    :return: A positive integer denoting the longest common subsequence
    """

    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")

    m = Matrix( len(lhs) + 1, len(rhs) + 1)

    for i, char1 in zip( range(1 , len(lhs) + 1), lhs ):
        for j, char2 in zip( range(1 , len(rhs) + 1), rhs ):
            if char1 == char2:
                m[ i, j ]  = m[ i - 1, j - 1 ] + 1
            else:
                m[ i, j ] = max( m[ i , j - 1 ], m[ i - 1, j ] )

    return m[ len(lhs), len(rhs) ]


def _get_prefix( lhs, rhs, max_prefix = 4 ):
    """
    
    :param lhs:
    :param rhs:
    :param max_prefix:
    :return:
    """
    length = min( len(lhs), min(rhs), max_prefix )

    for i in range( 0, length ):
        if lhs[i] != rhs[i]:
            return i
    return length

def _get_commons( lhs, rhs, dist ):
    """

    :param lhs:
    :param rhs:
    :param dist:
    :return:
    """
    commons = [ char for index, char in enumerate( lhs ) if char in rhs[ int( max( 0, index - dist ) ) : int( min( index + dist, len(rhs) ) ) ] ]
    return commons, len(commons)

def jaro_distance(lhs, rhs):
    """

    :param lhs:
    :param rhs:
    :return:
    """

    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")


    max_range = max( floor( float( max( len(lhs), len(rhs) ) ) / float( 2.0 ) ) - 1, 0)

    commons1, _len1 = _get_commons( lhs, rhs, max_range )
    commons2, _len2 = _get_commons( rhs, lhs, max_range )

    if _len1 == 0 or _len2 == 0:
        return 0

    num_transpositions = sum( ch1 != ch2 for ch1, ch2 in zip( commons1, commons2 ) ) / 2.0
    return ( _len1 / float(len(lhs)) + _len2 / float(len(rhs)) + ( _len1 - num_transpositions ) / float(_len1)  ) / 3.0

def jaro_winkler( lhs, rhs, prefix_scale = 0.1 ):
    """
    https://secure.wikimedia.org/wikipedia/en/wiki/Jaro%E2%80%93Winkler_distance

    :param lhs:
    :param rhs:
    :param prefix_scale:
    :return:
    """

    if not lhs or not rhs: raise ValueError("Input cannot be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")


    dist = jaro_distance( lhs, rhs )
    prefix = _get_prefix( lhs, rhs )
    return dist + (prefix * prefix_scale * ( 1 - dist ))

def dice_coefficient(lhs, rhs):
    """
    https://secure.wikimedia.org/wikipedia/en/wiki/Dice%27s_coefficient
    """

    if not lhs or not rhs: raise ValueError("Input can not be empty")
    if type(lhs) != type(rhs): raise ValueError("Input should be of the same type")


    if isinstance( lhs, (str, unicode) ) and isinstance( rhs, (str, unicode) ):
        #Generate the bigrams
        lhs =  [ lhs[index : index + 2 ] for index, _ in enumerate( lhs[0:-1] ) ]
        rhs =  [ rhs[index : index + 2 ] for index, _ in enumerate( rhs[0:-1] ) ]

    inter = len(set(lhs).intersection( set(rhs) ) )
    return ( 2 * inter ) / float( len(lhs) + len(rhs) )

def soundex( s ):
    """
    Implements the simplified Soundex algorithm.

    Implements American soundex
    https://secure.wikimedia.org/wikipedia/en/wiki/Soundex
    """

    if not s: raise ValueError("String can not be empty")
    if not isinstance( s, ( str, unicode ) ): raise ValueError("Input must be string or unicode")


    KEY_LENGTH = 4

    def to_digit( char ):
        digit = { 'B' : '1', 'F' : '1', 'P' : '1', 'V' : '1',
            'C' : '2', 'G' : '2', 'J' : '2', 'K' : '2', 'Q' : '2', 'S' : '2', 'X' : '2', 'Z' : '2',
            'D' : '3', 'T' : '3',
            'L' : '4',
            'M' : '5', 'N' : '5',
            'R' : '6' }
        try:
            return digit[char]
        except KeyError:
            return 0

    s = str(s).upper()
    s = re.sub(r'[^A-Z]+', '', s)


    code = s[0]
    digits = [ to_digit( char ) for char in s ] #encode as digits
    digits = [k for k, _ in itertools.groupby(digits)] #Remove all adjacent duplicates
    digits = [ digit for digit in digits if digit != 0 ] #Remove all 0s

    #if first letter was a coded as 0, it has been removed in previous steps
    if to_digit( code ) == 0:
        code += ''.join( digits )
    else:
        code += ''.join( digits[1:] )

    #Pad with 0 and return the 4 char key
    return (code + KEY_LENGTH*"0")[ :KEY_LENGTH ]


def nysiis(name, truncate=True):
    if not name: raise ValueError("Name can not be empty")
    if not isinstance( name, (str, unicode) ): raise ValueError("Name must be sting or unicode")

    vowels = ["A", "E", "I", "U", "O"]

    name = str(name).upper().strip()

    pre = [
        (r'\s+JR\.?\s{0,}', ''),
        (r'\s+SR\.?\s{0,}', ''),
        (r'\s+[IVXMC]+\.?\s{0,}', ''),
        ( r'[^A-Z]+', '' ),
        (r'^MAC', 'MCC'),
        (r'^KN', 'N'),
        (r'K', 'C'),
        (r'^P[HF]', 'FF'),
        (r'^SCH', 'SSS'),
        (r'[EI]E$', 'Y'),
        (r'[DRN]T$', 'D'),
        (r'[RN]D$', 'D')
    ]

    post = [
        (r'EV', 'AF'),
        (r'[AEIOU]', 'A'),
        (r'Q', 'G'),
        (r'Z', 'S'),
        (r'M', 'N'),
        (r'KN', 'N'),
        (r'K', 'C'),
        (r'SCH', 'SSS'),
        (r'PH', 'FF'),
        (r'([^%s])H' % ''.join( vowels ), r'\1'),
        (r'(.)H(?=[^%s])' % ''.join( vowels ), r'\1'),
        (r'[%s]W' % ''.join(vowels), 'A'),
        (r'S+$', ''),
        (r'AY$', 'Y'),
        (r'A+$', '')
    ]

    for reg, sub in pre:
        name = re.sub( reg, sub, name )

    try:
        code = name[0]
    except IndexError:
        raise ValueError("String is not encodable")

    name = name[1:]

    for reg, sub in post:
        name = re.sub( reg, sub, name )

    #remove all adjacent duplicates
    code += ''.join([key for key, _ in itertools.groupby(name)])

    if len( code ) > 6 and truncate:
        return code[:6]
    else:
        return code