import unittest
from  fuzzycomp import fuzzycomp
import sys


class TestLevenshteinDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.levenshtein_distance( "Hello", "Hello" ), 0 )
        self.assertEqual( fuzzycomp.levenshtein_distance( "Saturday", "Sunday" ), 3 ) #From wikipedia

    def test_case_difference(self):
        """Algorithm should be case sensitive"""
        self.assertNotEqual( fuzzycomp.levenshtein_distance( "HELLO", "hello" ), 0 )

    def test_invalid_input(self):
        """Function should raise ValueError if either string is empty"""
        self.assertRaises( ValueError, fuzzycomp.levenshtein_distance, "", "hello" )


class TestMatrix( unittest.TestCase ):
    def setUp(self):
        self.size = ( 4, 5 )
        self.m = fuzzycomp.Matrix( self.size[0], self.size[1] )

    def test_invalid_index(self):
        """Function should fail when index is out of range"""
        self.assertRaises( IndexError, self.m.__getitem__, (self.size[0] + 1, 0) )
        self.assertRaises( IndexError, self.m.__getitem__, (0, self.size[0] + 1) )

    def test_negative_index(self):
        """Function should fail when passed negative indexes"""
        self.assertRaises( IndexError, self.m.__getitem__, (-1, 0) )
        self.assertRaises( IndexError, self.m.__getitem__, (0, -1) )

    def test_size(self):
        """Size value should correspond to that used to create the Matrix"""
        self.assertTupleEqual( self.m.size(), self.size )

    def test_insertion(self):
        """Values should be properly stored in the Matrix"""
        for i in range( self.size[0] ):
            for j in range( self.size[1] ):
                self.m[ i, j ] = i+j

        for i in range( self.size[0] ):
            for j in range( self.size[1] ):
                self.assertEqual( self.m[ i, j ], i+j )

class TestJaccardDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.jaccard_distance( "Hello", "Hello" ), 0.0 )
        self.assertAlmostEqual( fuzzycomp.jaccard_distance( "Hello", "World" ), 0.7142857, 7 )
        self.assertEqual( fuzzycomp.jaccard_distance( "foo", "bar" ), 1.0 )

class TestSoerenseIndex( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.soerensen_index( "Hello", "Hello" ), 1.0 )
        self.assertEqual( fuzzycomp.soerensen_index( "foo", "bar" ), 0.0 )

class TestHammingDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.hamming_distance( "Hello", "Hello" ), 0.0 )
        self.assertEqual( fuzzycomp.hamming_distance( "Hello", "World" ), 4.0 )
        self.assertEqual( fuzzycomp.hamming_distance( "foo", "bar" ), 3.0 )

class TestLCS( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.lcs_length("XMJYAUZ", "MZJAWXU"), 4 )
        self.assertEqual( fuzzycomp.lcs_length("foo", "bar"), 0 )

class TestJaroDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""

class TestJaroWinklerDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""


class TestDiceCoefficient( unittest.TestCase ):
    def test_valid_input(self):
         """Algorithm should return correct values under valid input"""

class TestSoundex( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""

if __name__ == "__main__":
    sys.exit( unittest.main() )