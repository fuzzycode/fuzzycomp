# -*- coding: utf-8 -*-

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

class BaseTester( unittest.TestCase ):
    def mixed_iterable_input(self, func, error = ValueError):
        self.assertRaises( error, func, "Hello", [1,5] )
        self.assertRaises( error, func, [1,5], "Hello" )

        self.assertRaises( error, func, "Hello", (1,5) )
        self.assertRaises( error, func, (1,5), "Hello" )

        self.assertRaises( error, func, (1,5), [1,5] )
        self.assertRaises( error, func, [1,5], (1,5) )


    def empty_iterable_input(self, func, error = ValueError):
        self.assertRaises( error, func, "", "Hello" )
        self.assertRaises( error, func, "Hello", "" )

        self.assertRaises( error, func, [], [1,2] )
        self.assertRaises( error, func, [1,2], [] )

        self.assertRaises( error, func, tuple(), (1,2) )
        self.assertRaises( error, func, (1,2), tuple() )

class TestLevenshteinDistance( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.levenshtein_distance( "Hello", "Hello" ), 0 )
        self.assertEqual( fuzzycomp.levenshtein_distance( "Saturday", "Sunday" ), 3 )

    def test_case_difference(self):
        """Algorithm should be case sensitive"""
        self.assertNotEqual( fuzzycomp.levenshtein_distance( "HELLO", "hello" ), 0 )

    def test_empty_input(self):
        """Function should raise ValueError if either input is empty"""
        self.empty_iterable_input( fuzzycomp.levenshtein_distance )

    def test_iterable_input(self):
        """Function should function properly when called with an iterable"""
        self.assertEqual( fuzzycomp.levenshtein_distance( ["H", "e", "l", "l", "o"],
            ["H", "e", "l", "l", "o"] ), 0 )

        self.assertEqual( fuzzycomp.levenshtein_distance( ["S", "a", "t", "u", "r", "d", "a", "y"],
                                                        ["S", "u", "n", "d", "a", "y"] ), 3 )

        self.assertEqual( fuzzycomp.levenshtein_distance( ("H", "e", "l", "l", "o"),
            ("H", "e", "l", "l", "o") ), 0 )

        self.assertEqual( fuzzycomp.levenshtein_distance( ("S", "a", "t", "u", "r", "d", "a", "y"),
                                                        ("S", "u", "n", "d", "a", "y") ), 3 )

    def test_mixed_input(self):
        """Function should raise value error if passed with mixed types"""
        self.mixed_iterable_input( fuzzycomp.levenshtein_distance )

class TestMatrix( unittest.TestCase ):
    def setUp(self):
        self.size = ( 4, 5 )
        self.m = fuzzycomp.Matrix( self.size[0], self.size[1] )

    def test_negative_size(self):
        """Function should fail when creating a matrix with negative size"""
        self.assertRaises( ValueError, fuzzycomp.Matrix, -1, -1 )
        self.assertRaises( ValueError, fuzzycomp.Matrix, -1, 5 )
        self.assertRaises( ValueError, fuzzycomp.Matrix, 7, -1 )

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
        self.assertEqual( self.m.size(), self.size )

    def test_insertion(self):
        """Values should be properly stored in the Matrix"""
        for i in range( self.size[0] ):
            for j in range( self.size[1] ):
                self.m[ i, j ] = i+j

        for i in range( self.size[0] ):
            for j in range( self.size[1] ):
                self.assertEqual( self.m[ i, j ], i+j )

class TestJaccardDistance( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.jaccard_distance( "Hello", "Hello" ), 0.0 )
        self.assertAlmostEqual( fuzzycomp.jaccard_distance( "Hello", "World" ), 0.7142857, 7 )
        self.assertEqual( fuzzycomp.jaccard_distance( "foo", "bar" ), 1.0 )

    def test_iterable_input(self):
        """Function should return correct values when called with valid iterables"""
        self.assertEqual( fuzzycomp.jaccard_distance( [1 ,2, 3, 4, 5], [5, 4, 3, 2, 1] ), 0.0 )
        self.assertEqual( fuzzycomp.jaccard_distance( [1 ,2, 3, 4, 5], [6, 7, 8, 9, 10] ), 1.0 )

    def test_empty_input(self):
        """function should raise ValueError if called with empty iterable"""
        self.empty_iterable_input( fuzzycomp.jaccard_distance )

    def test_mixed_input(self):
        """function should raise ValueError if input is of mixed type"""
        self.mixed_iterable_input( fuzzycomp.jaccard_distance )

class TestHammingDistance( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.hamming_distance( "Hello", "Hello" ), 0.0 )
        self.assertEqual( fuzzycomp.hamming_distance( "Hello", "World" ), 4.0 )
        self.assertEqual( fuzzycomp.hamming_distance( "foo", "bar" ), 3.0 )

    def test_input_of_various_lengths(self):
        """Function should raise ValueError if both inputs are not equal length"""
        self.assertRaises( ValueError, fuzzycomp.hamming_distance, "Hello", "Goodbye" )
        
    def test_empty_input(self):
        """Function should raise ValueError if called with empty input"""
        self.empty_iterable_input( fuzzycomp.hamming_distance )

    def test_iterable_input(self):
        """Function should return correct values when called with valid iterables as input"""
        self.assertEqual( fuzzycomp.hamming_distance( ["H", "e", "l", "l", "o"],
                                                    ["H", "e", "l", "l", "o"] ), 0.0 )
        self.assertEqual( fuzzycomp.hamming_distance( ["H", "e", "l", "l", "o"],
                                                        ["W", "o", "r", "l", "d"] ), 4.0 )
        self.assertEqual( fuzzycomp.hamming_distance( ["f", "o", "o"], ["b", "a", "r"] ), 3.0 )

        self.assertEqual( fuzzycomp.hamming_distance( ("H", "e", "l", "l", "o"),
                                                    ("H", "e", "l", "l", "o") ), 0.0 )
        self.assertEqual( fuzzycomp.hamming_distance( ("H", "e", "l", "l", "o"),
                                                        ("W", "o", "r", "l", "d") ), 4.0 )
        self.assertEqual( fuzzycomp.hamming_distance( ("f", "o", "o"), ("b", "a", "r") ), 3.0 )


    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.mixed_iterable_input( fuzzycomp.hamming_distance )
        self.assertRaises( ValueError, fuzzycomp.hamming_distance, "Foo", [1, 2, 3] )
        self.assertRaises( ValueError, fuzzycomp.hamming_distance, [1, 2, 3], "Foo" )


class TestLCS( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertEqual( fuzzycomp.lcs_length("XMJYAUZ", "MZJAWXU"), 4 )
        self.assertEqual( fuzzycomp.lcs_length("foo", "bar"), 0 )
           
    def test_empty_input(self):
        """Function should raise ValueError if called with empty input"""
        self.empty_iterable_input( fuzzycomp.lcs_length )

    def test_iterable_input(self):
        """Function should return correct values when called with valid iterables as input"""
        self.assertEqual( fuzzycomp.lcs_length(["X", "M", "J", "Y", "A", "U", "Z"],
            ["M", "Z", "J", "A", "W", "X", "U"]), 4 )
        self.assertEqual( fuzzycomp.lcs_length(["f", "o", "o"], ["b", "a", "r"]), 0 )

        self.assertEqual( fuzzycomp.lcs_length(("X", "M", "J", "Y", "A", "U", "Z"),
            ("M", "Z", "J", "A", "W", "X", "U")), 4 )
        self.assertEqual( fuzzycomp.lcs_length(("f", "o", "o"), ("b", "a", "r")), 0 )


    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.mixed_iterable_input( fuzzycomp.lcs_length )

class TestJaroDistance( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "MARTHA", "MARHTA" ), 0.944, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "DWAYNE", "DUANE" ), 0.822, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( "DIXON", "DICKSONX" ), 0.767, places=3  )

    def test_empty_input(self):
        """Function should raise ValueError if passed an empty input"""
        self.empty_iterable_input( fuzzycomp.jaccard_distance )

    def test_iterable_input(self):
        """Function should raise ValueError if passed non string input"""
        self.assertAlmostEqual( fuzzycomp.jaro_distance( ["M", "A", "R", "T", "H", "A"],
            ["M", "A", "R", "H", "T", "A"] ), 0.944,  places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( ["D", "W", "A", "Y", "N", "E"],
            ["D", "U", "A", "N", "E"] ), 0.822, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( ["D", "I", "X", "O", "N"],
            ["D", "I", "C", "K", "S", "O", "N", "X"] ), 0.767,  places=3  )


        self.assertAlmostEqual( fuzzycomp.jaro_distance( ("M", "A", "R", "T", "H", "A"),
            ("M", "A", "R", "H", "T", "A") ), 0.944,  places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( ("D", "W", "A", "Y", "N", "E"),
            ("D", "U", "A", "N", "E") ), 0.822, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_distance( ("D", "I", "X", "O", "N"),
            ("D", "I", "C", "K", "S", "O", "N", "X") ), 0.767,  places=3  )

    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.mixed_iterable_input( fuzzycomp.jaro_distance )

class TestJaroWinklerDistance( BaseTester ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "MARTHA", "MARHTA" ), 0.961, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "DWAYNE", "DUANE" ), 0.84, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( "DIXON", "DICKSONX" ), 0.813, places=3  )

    def test_empty_input(self):
        """Function should raise ValueError if passed an empty input"""
        self.empty_iterable_input( fuzzycomp.jaro_winkler )

    def test_iterable_input(self):
        """Function should raise ValueError if passed non string input"""
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ["M", "A", "R", "T", "H", "A"],
            ["M", "A", "R", "H", "T", "A"] ), 0.961, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ["D", "W", "A", "Y", "N", "E"],
            ["D", "U", "A", "N", "E"] ), 0.84, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ["D", "I", "X", "O", "N"],
            ["D", "I", "C", "K", "S", "O", "N", "X"] ), 0.813, places=3  )

        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ("M", "A", "R", "T", "H", "A"),
            ("M", "A", "R", "H", "T", "A") ), 0.961, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ("D", "W", "A", "Y", "N", "E"),
            ("D", "U", "A", "N", "E") ), 0.84, places=3  )
        self.assertAlmostEqual( fuzzycomp.jaro_winkler( ("D", "I", "X", "O", "N"),
            ("D", "I", "C", "K", "S", "O", "N", "X") ), 0.813, places=3  )

    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.mixed_iterable_input( fuzzycomp.jaro_winkler )

class TestDiceCoefficient( BaseTester ):
    def test_valid_input(self):
         """Algorithm should return correct values under valid input"""
         self.assertEqual( fuzzycomp.dice_coefficient( "night", "nacht" ), 0.25 )

    def test_empty_input(self):
        """Function should raise ValueError if called with empty input"""
        self.empty_iterable_input( fuzzycomp.dice_coefficient )

    def test_iterable_input(self):
        """Function should return correct values when called with valid iterables as input"""
        self.assertEqual( fuzzycomp.dice_coefficient( ["ni", "ig", "gh", "ht"],
            ["na", "ac",  "ch", "ht"] ),  0.25 )

        self.assertEqual( fuzzycomp.dice_coefficient( ("ni", "ig", "gh", "ht"),
            ("na", "ac",  "ch", "ht") ),  0.25 )

    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.mixed_iterable_input( fuzzycomp.dice_coefficient )

class TestTverskyIndex( unittest.TestCase ):
    def test_valid_input(self):
        """Function should return correct values under valid input"""
        self.assertEqual(fuzzycomp.tversky_index("Hello", "Hello", 1.0, 1.0), 1.0 )
        self.assertEqual(fuzzycomp.tversky_index("foo", "bar", 1.0, 1.0), 0.0 )


    def test_case_sensitive(self):
        """Function should be case sensitive"""
        self.assertNotEqual( fuzzycomp.tversky_index("hello", "HELLO", 1.0, 1.0), 1.0 )


    def test_non_zero_parameters(self):
        """Function should raise ValueError if alpha or beta <= 0"""
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", 0, 0.5 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", 0.5, 0.0 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", 0.0, 0.0 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", -0.5, 0.5 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", 0.5, -1.0 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "World", -0.5, -2.0 )

    def test_dice_similarity(self):
        """If alpha=beta=0.5 function should produce the same result as Dice Coefficient"""
        self.assertEqual( fuzzycomp.tversky_index("night", "nacht", 0.5, 0.5),
            fuzzycomp.dice_coefficient("night", "nacht") )

    def test_empty_input(self):
        """Function should raise ValueError if called with empty input"""
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "", "Hello", 1.0, 1.5 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", "", 0.2, 0.7 )

        self.assertRaises( ValueError, fuzzycomp.tversky_index, [], [1,2], 0.4, 1.5 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, [1,2], [], 1.6, 0.7 )

        self.assertRaises( ValueError, fuzzycomp.tversky_index, tuple(), (1,2), 0.9, 0.7 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, (1,2), tuple(), 0.7, 0.7 )

    def test_iterable_input(self):
        """Function should return correct values when called with valid iterables as input"""
        self.assertEqual(fuzzycomp.tversky_index(["He", "el", "ll", "lo"],
            ["He", "el", "ll", "lo"], 1.0, 1.0),  1.0 )
        self.assertEqual(fuzzycomp.tversky_index(["fo", "oo"], ["ba", "ar"], 1.0, 1.0), 0.0 )

        self.assertEqual(fuzzycomp.tversky_index(("He", "el", "ll", "lo"),
            ("He", "el", "ll", "lo"), 1.0, 1.0),  1.0 )
        self.assertEqual(fuzzycomp.tversky_index(("fo", "oo"), ("ba", "ar"), 1.0, 1.0), 0.0 )


    def test_mixed_input(self):
        """Function should raise ValueError if called with mixed input"""
        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", [1,5], 0.8, 0.8 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, [1,5], "Hello", 0.3, 1.4 )

        self.assertRaises( ValueError, fuzzycomp.tversky_index, "Hello", (1,5), 1.5, 1.4 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, (1,5), "Hello", 1.0, 1.0 )

        self.assertRaises( ValueError, fuzzycomp.tversky_index, (1,5), [1,5], 0.5, 0.5 )
        self.assertRaises( ValueError, fuzzycomp.tversky_index, [1,5], (1,5), 4, 8 )


class TestSoundex( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        data = [ ('HERMAN', 'H650'), ('Robert', 'R163'), ('Rupert', 'R163'), ('Rubin', 'R150'),
            ('Ashcraft', 'A261'), ('Ashcroft', 'A261') ]

        for d in data:
            self.assertEqual( fuzzycomp.soundex( d[0] ), d[1] )

    def test_same_code(self):
        """All listed names should produce the same soundex code"""
        name_lists = [
        ]

        for names in name_lists:
            code = fuzzycomp.soundex( names[0] )
            for name in names:
                self.assertEqual( fuzzycomp.soundex( name ), code )

    def test_ignore_trimmables(self):
        """Function should ignore white-space before and after the word"""
        self.assertEqual( fuzzycomp.soundex("Rubin"), fuzzycomp.soundex("\t\r\n  Rubin \t\r\n") )

    def test_empty_string(self):
        """function should raise ValueError when provided with an empty string"""
        self.assertRaises( ValueError, fuzzycomp.soundex, "" )

    def test_non_string(self):
        """function should raise ValueError when provided with a value that is not a string"""
        data = [ 2,
                [2, 3, 6],
                ["hello", "world"],
                {"Hello" : "World"} ]
        
        for d in data:
            self.assertRaises( ValueError, fuzzycomp.soundex, d )


    def test_ignore_bad_chars(self):
        """Un-encodable  characters should be ignored"""
        strings = [ "HOLMES", "H-OLMES", "HO-LMES", "HOL-MES", "HOLM-ES", "HOLME-S", "HOLMES-" ]
        result = "H452"

        for s in strings:
            self.assertEqual( fuzzycomp.soundex(s), result )

        self.assertEqual( fuzzycomp.soundex("HOL>MES"), result )
        self.assertEqual( fuzzycomp.soundex("HOLM<ES"), result )
        self.assertEqual( fuzzycomp.soundex("HOL|MES"), result )

        for s in ["'OBrien", "'OBrien", "O'Brien", "OB'rien", "OBr'ien", "OBri'en", "OBrie'n",
                  "OBrien'"]:
            self.assertEqual( fuzzycomp.soundex( s ), "O165" )


    def test_case_insensitive(self):
        """Function should be case insensitive"""
        names = ["Robert", "Rupert", "Rubin", "Ashcraft", "Ashcroft"]

        for name in names:
            self.assertEqual( fuzzycomp.soundex(name.lower()), fuzzycomp.soundex( name.upper() ) )

class TestNYSIIS( unittest.TestCase ):
    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""

        #Test case from http://dropby.com/NYSIISTextStrings.html
        names = [
            ("MACINTOSH", "MCANT"),
            ("KNUTH", "NNAT"),
            ("KOEHN", "C"),
            ("PHILLIPSON", "FFALAP"),
            ("PFEISTER", "FFASTA"),
            ("SCHOENHOEFT", "SSANAF"),
            ("MCKEE", "MCY"),
            ("MACKIE", "MCY"),
            ("HEITSCHMIDT", "HATSNA"),
            ("BART", "BAD"),
            ("HURD", "HAD"),
            ("HUNT", "HAD"),
            ("WESTERLUND", "WASTAR"),
            ("CASSTEVENS", "CASTAF"),
            ("VASQUEZ", "VASG"),
            ("FRAZIER", "FRASAR"),
            ("BOWMAN", "BANAN"),
            ("MCKNIGHT", "MCNAGT"),
            ("RICKERT", "RACAD"),
            ("DEUTSCH", "DATS"),
            ("WESTPHAL", "WASTFA"),
            ("SHRIVER", "SHRAVA"),
            ("KUHL", "C"),
            ("RAWSON", "RASAN"),
            ("JILES", "JAL"),
            ("CARRAWAY", "CARAY"),
            ("YAMADA", "YANAD"),
        ]

        for name in names:
            self.assertEquals( fuzzycomp.nysiis( name[0] ), name[1] )


    def test_non_truncated(self):
        """If not truncated, the function should return codes longer than 6"""
        names = [
            ("PHILLIPSON", "FFALAPSAN"),
            ("PFEISTER", "FFASTAR"),
            ("SCHOENHOEFT", "SSANAFT"),
            ("HEITSCHMIDT", "HATSNAD"),
            ("WESTERLUND", "WASTARLAD"),
            ("CASSTEVENS", "CASTAFAN"),
            ("WESTPHAL", "WASTFAL"),
            ("SHRIVER", "SHRAVAR"),
            ("CARRAWAY", "CARAY"),
            ("YAMADA", "YANAD"),
        ]

        for name in names:
            self.assertEquals( fuzzycomp.nysiis( name[0], False ), name[1] )


    def test_JR(self):
        """function should handle the presence of Jr correctly """
        names = [
            ("BART Jr.", "BAD"),
            ("HURD JR", "HAD"),
            ("HUNT JR.", "HAD"),
        ]
        
        for name in names:
            self.assertEquals( fuzzycomp.nysiis( name[0], False ), name[1] )


    def test_romans(self):
        """Function should handle the presence of roman numbers in the name correctly"""
        names = [
            ("BART I", "BAD"),
            ("HURD III", "HAD"),
            ("HUNT IV.", "HAD"),

            ("BART M", "BAD"),
            ("HURD C", "HAD"),
            ("HUNT X.", "HAD"),

            ("BART II", "BAD"),
            ("HURD MC", "HAD"),
            ("HUNT XV.", "HAD"),
        ]

        for name in names:
            self.assertEquals( fuzzycomp.nysiis( name[0], False ), name[1] )

    def test_empty_string(self):
        """function should raise ValueError when provided with an empty string"""
        self.assertRaises( ValueError, fuzzycomp.nysiis, "" )

    def test_non_string(self):
        """function should raise ValueError when provided with a value that is not a string"""
        data = [ 2,
                [2, 3, 6],
                ["hello", "world"],
                {"Hello" : "World"} ]

        for d in data:
            self.assertRaises( ValueError, fuzzycomp.nysiis, d )

    def test_non_codable_input(self):
        """Function should raise ValueError if passed a string that can not be encoded"""
        self.assertRaises( ValueError, fuzzycomp.nysiis, "!&€/)€%&" )
        self.assertRaises( ValueError, fuzzycomp.nysiis, "?" )

        for s in '!"#€%&/()=?´`*-.:,;<>§°^~':
            self.assertRaises( ValueError, fuzzycomp.nysiis, s )

    def test_case_insensitive(self):
        """Function should be case insensitive"""
        names = ["Robert", "Rupert", "Rubin", "Ashcraft", "Ashcroft"]

        for name in names:
            self.assertEqual( fuzzycomp.nysiis(name.lower()), fuzzycomp.nysiis( name.upper() ) )


class TestMetaphone(unittest.TestCase):
    def setUp(self):
        self.names =  [
            ("ANASTHA",             "ANS0"),
            ("DAVIS-CARTER",        "TFSK"),
            ("ESCARMANT",           "ESKR"),
            ("MCCALL",              "MKL"),
            ("MCCROREY",            "MKRR"),
            ("MERSEAL",             "MRSL"),
            ("PIEURISSAINT",        "PRSN"),
            ("ROTMAN",              "RTMN"),
            ("SCHEVEL",             "SXFL"),
            ("SCHROM",              "SXRM"),
            ("SEAL",                "SL"),
            ("SPARR",               "SPR"),
            ("STARLEPER",           "STRL"),
            ("THRASH",              "0RX"),
            ("ANASTHA",             "ANS0"),
            ("DAVIS-CARTER",        "TFSK"),
            ("ESCARMANT",           "ESKR"),
            ("MCCALL",              "MKL"),
            ("MCCROREY",            "MKRR"),
            ("MERSEAL",             "MRSL"),
            ("PIEURISSAINT",        "PRSN"),
            ("ROTMAN",              "RTMN"),
            ("SCHEVEL",             "SXFL"),
            ("SCHROM",              "SXRM"),
            ("SEAL",                "SL"),
            ("SPARR",               "SPR"),
            ("STARLEPER",           "STRL"),
            ("THRASH",              "0RX"),
            ("LOGGING",             "LKKN"),
            ("LOGIC",               "LJK"),
            #("JUDGES",             "JJS"),
            ("SHOOS",               "XS"),
            ("SHOES",               "XS"),
            ("CHUTE",               "KHT"),
            ("SCHUSS",              "SXS"),
            ("OTTO",                "OT"),
            ("ERIC",                "ERK"),
            ("DAVE",                "TF"),
            ("CATHERINE",           "K0RN"),
            ("KATHERINE",           "K0RN"),
            ("AUBREY",              "ABR"),
            ("BRYAN",               "BRYN"),
            ("BRYCE",               "BRS"),
            ("STEVEN",              "STFN"),
            ("RICHARD",             "RXRT"),
            ("HEIDI",               "HT"),
            ("AUTO",                "AT"),
            ("MAURICE",             "MRS"),
            ("RANDY",               "RNT"),
            ("CAMBRILLO",           "KMBR"),
            ("BRIAN",               "BRN"),
            ("RAY",                 "R"),
            ("GEOFF",               "JF"),
            ("BOB",                 "BB"),
            ("AHA",                 "AH"),
            ("AAH",                 "A"),
            ("PAUL",                "PL"),
            ("BATTLEY",             "BTL"),
            ("WROTE",               "RT"),
            ("THIS",                "0S"),
        ]

    def test_valid_input(self):
        """Algorithm should return correct values under valid input"""
        for name in self.names:
            self.assertEquals( fuzzycomp.metaphone( name[0] ), name[1])

    def test_unicode(self):
        """Function should return valid results when passed valid unicode data"""
        for name in self.names:
            self.assertEquals( fuzzycomp.metaphone( unicode(name[0]) ), name[1])

    def test_negative_length(self):
        """Function should raise ValueError if passed a length <= 0"""
        self.assertRaises( ValueError, fuzzycomp.metaphone,  "Paul", -1 )
        self.assertRaises( ValueError, fuzzycomp.metaphone,  "Paul", 0 )

    def test_non_int_length(self):
        """Function should raise ValueError if the length argument is not an integer"""
        self.assertRaises( ValueError, fuzzycomp.metaphone, "PAUL", 1.2 )
        self.assertRaises( ValueError, fuzzycomp.metaphone, "PAUL", 0.2 )
        self.assertRaises( ValueError, fuzzycomp.metaphone, "PAUL", 5.2 )
        self.assertRaises( ValueError, fuzzycomp.metaphone, "PAUL", 12.2 )

    def test_longer_codes(self):
        """Function should return correct values when longer codes are used"""
        self.assertEqual( fuzzycomp.metaphone( "DAVIS-CARTER", 7 ), "TFSKRTR" )
        self.assertEqual( fuzzycomp.metaphone( "DAVIS-CARTER", 6 ), "TFSKRT" )
        self.assertEqual( fuzzycomp.metaphone( "DAVIS-CARTER", 5 ), "TFSKR" )
        self.assertEqual( fuzzycomp.metaphone( "ESCARMANT", 7 ), "ESKRMNT" )
        self.assertEqual( fuzzycomp.metaphone( "STARLEPER", 6 ), "STRLPR" )
        self.assertEqual( fuzzycomp.metaphone( "CAMBRILLO", 5 ), "KMBRL" )
        self.assertEqual( fuzzycomp.metaphone( "BRYCE", 7 ), "BRS" )

    def test_empty_string(self):
        """function should raise ValueError when provided with an empty string"""
        self.assertRaises( ValueError, fuzzycomp.metaphone, "" )

    def test_non_encodable_chars(self):
        """Non-encodable chars should be ignored"""
        names = ["-testing", "t-esting", "te-sting", "tes-ting", "test-ing", "testi-ng",
                 "testin-g", "testing-"]
        key = "TSTN"
        for name in names:
            self.assertEquals( fuzzycomp.metaphone(name), key )

        self.assertEquals( fuzzycomp.metaphone("test>ing"), key )

    def test_non_encodable_strings(self):
        """Function should return an empty string if it can not be encoded"""
        self.assertEqual( fuzzycomp.metaphone("!&(#=#/%#?+§"), "" )
        for char in "!&(#=#/%#?+§":
            self.assertEqual( fuzzycomp.metaphone(char), "" )


    def test_non_string(self):
        """function should raise ValueError when provided with a value that is not a string"""
        data = [ 2,
                [2, 3, 6],
                ["hello", "world"],
                {"Hello" : "World"} ]

        for d in data:
            self.assertRaises( ValueError, fuzzycomp.metaphone, d )

    def test_trimmable_chars(self):
        """Function should ignore trimmable chars in front and after the string"""
        names = [
            ("\r\t\n       RANDY \r\t\n    ",               "RNT"),
            ("\r\t\n    CAMBRILLO\r\t\n    ",           "KMBR"),
            ("\r\t\n    BRIAN\r\t\n    ",               "BRN"),
            ("\r\t\n    RAY\r\t\n    ",                 "R")
        ]
        for name in names:
            self.assertEquals( fuzzycomp.metaphone( name[0] ), name[1] )


    def test_equal_code(self):
        """All listed names should produce the same Metaphone key"""

        name_list = [
            ("White", "Wade", "Wait", "Waite", "Wat", "Whit", "Wiatt", "Wit", "Wittie", "Witty"),
            ("Albert","Ailbert", "Alberik", "Albert", "Alberto" ),
            ("Gary","Carie", "Caro", "Carree", "Carri", "Carrie", "Carry","Cary","Cora","Corey",
             "Cori", "Corie", "Correy"),
            ("John", "Gina", "Ginni","Ginnie","Ginny","Jaine","Jan","Jana","Jane","Janey",
             "Jania","Janie","Janna","Jany","Jayne"),
            ("Knight", "Nat","Nata","Natty","Neda","Nedda","Nedi","Netta", "Netti"),
            ("Mary", "Mari", "Maria","Marie","Mary","Maura","Maure","Meara","Merrie","Merry",
             "Mira","Moira"),
            ("Paris", "Pearcy", "Perris", "Piercy", "Pierz", "Pryse"),
            ("Peter","Peadar", "Peder", "Pedro", "Peter", "Petr", "Peyter", "Pieter", "Pietro"),
            ("Ray", "Ray", "Rey", "Roi", "Roy", "Ruy" ),
            ("Susan","Susan", "Susana","Susann","Susanna","Susannah","Susanne","Suzann"),
            ("Wright","Rota", "Rudd", "Ryde"),
            ("Xalan", "Selena", "Selene", "Selina", "Seline","Suellen")
        ]

        for names in name_list:
            code = fuzzycomp.metaphone( names[0] )
            for name in names:
                _c = fuzzycomp.metaphone( name )
                self.assertEquals( _c, code )

    def test_case_insensitive(self):
        """Function should be case insensitive"""
        names = ["Wade", "Wait", "Alberik", "Albert", "Cari", "Caria", "Ginnie", "Ginny", "Nat",
                 "Nata", "Natty", "Meara", "Merrie", "Pearcy", "Perris", "Susana", "Susann",
                 "Rudd", "Ryde", "Selena", "Selene" ]

        for name in names:
            self.assertEqual( fuzzycomp.metaphone(name.lower()), fuzzycomp.metaphone( name.upper() ) )

class TestColognePhonetic( unittest.TestCase ):
    def setUp(self):
        self.names = [
            ("Breschnew", "17863"),
            (u"Müller-Lüdenscheidt", "65752682")
        ]

    def test_fummy(self):
        #raise NotImplementedError()
        pass

    def test_valid_input(self):
        """Function should return valid results under valid input"""
        for name in self.names:
            self.assertEqual( fuzzycomp.cologne_phonetic( name[0] ), name[1] )

    def test_unicode(self):
        """Function should work properly with Unicode data"""
        for name in self.names:
            self.assertEqual( fuzzycomp.cologne_phonetic( unicode(name[0]) ), name[1] )


    def test_non_string(self):
        """Function should raise ValueError when provided with input not being str or unicode"""
        data = [ 2,
                [2, 3, 6],
                ["hello", "world"],
                {"Hello" : "World"} ]

        for d in data:
            self.assertRaises( ValueError, fuzzycomp.cologne_phonetic, d )

    def test_empty_input(self):
        """Function should raise ValueError when provided with empty input"""
        self.assertRaises( ValueError, fuzzycomp.cologne_phonetic, "" )

    def test_case(self):
        """Function should be case insensitive"""
        self.assertEqual( fuzzycomp.cologne_phonetic("breschnew"),
                          fuzzycomp.cologne_phonetic("BRESCHNEW") )

    def test_non_encodable_strings(self):
        """Function should return an empty string if it can not be encoded"""
        self.assertEqual( fuzzycomp.cologne_phonetic("!%&)#=&#"), "" )

    def test_non_encodable_chars(self):
        """Non-encodable chars should be ignored"""
        self.assertEqual( fuzzycomp.cologne_phonetic("Müller-Lüdenscheidt"), "65752682" )

    def test_umlauts(self):
        """Umlauts should be ignored"""
        self.assertEqual( fuzzycomp.cologne_phonetic("Müller-Lüdenscheidt"), "65752682" )

    def test_trimmable_chars(self):
        """Whitespace should be removed in front and after the name"""
        self.assertEqual( fuzzycomp.cologne_phonetic("\t\n  Breschnew \t\n  "), "17863" )

print("Running tests")
if __name__ == "__main__":
    print("Running tests2")
    sys.exit( unittest.main() )