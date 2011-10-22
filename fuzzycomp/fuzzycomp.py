from exceptions import IndexError, ValueError
from math import floor

__all__ = ["levenshtein_distance", "jaccard_distance", "soerensen_index", "hamming_distance",
           "lcs_length", "jaro_distance", "jaro_winkler" ]

class Matrix(object):
    def __init__(self, rows, cols, default = 0):
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
    The comparison is case insensitive.

    See Wikipedia_ for more info on the Levenshtein distance.
    .. _Wikipedia : https://secure.wikimedia.org/wikipedia/en/wiki/Levenshtein_distance

    :param lhs: First string
    :param rhs: Second string
    :return: An integer representing the distance between the strings. The lower value the better
     match. 0 indicates a perfect match.
    :raise: ValueError if any of the strings is empty.
    """

    if not lhs or not rhs:
        raise ValueError("Strings can not be empty")

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
    dist = jaro_distance( lhs, rhs )
    prefix = _get_prefix( lhs, rhs )
    return dist + (prefix * prefix_scale * ( 1 - dist ))

def dice_coefficient(lhs, rhs):
    """
    https://secure.wikimedia.org/wikipedia/en/wiki/Dice%27s_coefficient
    """

    #Generate the bigrams
    lhsbi =  [ lhs[index : index + 2 ] for index, _ in enumerate( lhs[0:-1] ) ]
    rhsbi =  [ rhs[index : index + 2 ] for index, _ in enumerate( rhs[0:-1] ) ]

    inter = len(set(lhsbi).intersection( set(rhsbi) ) )
    return ( 2 * inter ) / float( len(lhsbi) + len(rhsbi) )

def soundex( s ):
    """
    Implements American soundex
    https://secure.wikimedia.org/wikipedia/en/wiki/Soundex
    """
    KEY_LENGTH = 4

    discard = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y']
    digit = { 'b' : '1', 'f' : '1', 'p' : '1', 'v' : '1',
              'c' : '2', 'g' : '2', 'j' : '2', 'k' : '2', 'q' : '2', 's' : '2', 'x' : '2', 'z' : '2',
              'd' : '3', 't' : '3',
              'l' : '4',
              'm' : '5', 'n' : '5',
              'r' : '6' }

    soundx = s[0]
    for char in s[1:]:
        if not char in discard and soundx[-1] != digit[ char ] and len(soundx) < KEY_LENGTH:
            soundx += digit[char]

    #Pad with 0 if resulting key is too short
    while len(soundx) < KEY_LENGTH:
        soundx += '0'

    return soundx