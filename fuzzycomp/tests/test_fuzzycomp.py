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

import unittest
from  fuzzycomp import fuzzycomp
import sys


#TODO: Both algorithms depending on the Matrix could be optimized to not use a Matrix at all,
# this saves us the superfluous implementation of a Matrix and should save us a lot of memory,
# especially for long sequences

#TODO: All algorithms work fine for valid input, but should all tests should be extended to do
# exhaustive testing of invalid input as well.



class TestLevenshteinDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.levenshtein_distance( "Hello", "Hello" ), 0 )
        self.assertEqual( fuzzycomp.levenshtein_distance( "Saturday", "Sunday" ), 3 )

    def test_case_difference(self):
        """Algorithm should be case sensitive"""
        self.assertNotEqual( fuzzycomp.levenshtein_distance( "HELLO", "hello" ), 0 )

    def test_empty_string_input(self):
        """Function should raise ValueError if either string is empty"""
        self.assertRaises( ValueError, fuzzycomp.levenshtein_distance, "", "hello" )
        self.assertRaises( ValueError, fuzzycomp.levenshtein_distance, "hello", "" )


class TestMatrix( unittest.TestCase ):
    def setUp(self):
        self.size = ( 4, 5 )
        self.m = fuzzycomp.Matrix( self.size[0], self.size[1] )

    def test_negative_size(self):
        """Function should fail when creating a matrix with negative size"""
        self.assertRaises( ValueError, fuzzycomp.Matrix, -1, -1 )

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

class TestSoerensenIndex( unittest.TestCase ):
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

    def test_strings_of_various_lengths(self):
        """Function should raise ValueError if both strings are not equal length"""
        self.assertRaises( ValueError, fuzzycomp.hamming_distance, "Hello", "Goodbye" )

class TestLCS( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.lcs_length("XMJYAUZ", "MZJAWXU"), 4 )
        self.assertEqual( fuzzycomp.lcs_length("foo", "bar"), 0 )

class TestJaroDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "MARTHA", "MARHTA" ), 0.944, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "DWAYNE", "DUANE" ), 0.822, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "DIXON", "DICKSONX" ), 0.767, places=3  )

class TestJaroWinklerDistance( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "MARTHA", "MARHTA" ), 0.961, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "DWAYNE", "DUANE" ), 0.84, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "DIXON", "DICKSONX" ), 0.813, places=3  )

class TestDiceCoefficient( unittest.TestCase ):
    def test_valid_input(self):
         """Algorithm should return correct values under valid input"""
         self.assertEqual( fuzzycomp.dice_coefficient( "night", "nacht" ), 0.25 )


class TestSoundex( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.soundex( "Robert" ), "R163" )
        self.assertEqual( fuzzycomp.soundex( "Rupert" ), "R163" )
        self.assertEqual( fuzzycomp.soundex( "Rubin" ), "R150" )
        self.assertEqual( fuzzycomp.soundex( "Ashcraft" ), "A261" )
        self.assertEqual( fuzzycomp.soundex( "Ashcroft" ), "A261" )
        

if __name__ == "__main__":
    sys.exit( unittest.main() )