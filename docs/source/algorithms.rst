Algorithms
==========

Comparison
----------
  .. autofunction:: fuzzycomp.levenshtein_distance
  .. autofunction:: fuzzycomp.jaccard_distance
  .. autofunction:: fuzzycomp.hamming_distance
  .. autofunction:: fuzzycomp.lcs_length
  .. autofunction:: fuzzycomp.jaro_distance
  .. autofunction:: fuzzycomp.jaro_winkler
  .. autofunction:: fuzzycomp.dice_coefficient
  .. autofunction:: fuzzycomp.tversky_index


Phonetic
--------
  .. autofunction:: fuzzycomp.soundex
  .. autofunction:: fuzzycomp.nysiis
  .. autofunction:: fuzzycomp.metaphone
  .. autofunction:: fuzzycomp.cologne_phonetic

Examples
--------
Using some of the comparison algorithms::

    >>> from fuzzycomp import fuzzycomp
    >>> fuzzycomp.levenshtein_distance("Saturday", "Sunday")
    3
    >>> fuzzycomp.jaccard_distance( "Hello", "World" )
    0.7142857142857143
    >>> fuzzycomp.lcs_length("XMJYAUZ", "MZJAWXU")
    4
    >>> fuzzycomp.jaro_winkler( "DWAYNE", "DUANE" )
    0.8400000000000001

And for the phonetic algorithms::

    >>> from fuzzycomp import fuzzycomp
    >>> fuzzycomp.soundex("HERMAN")
    'H650'
    >>> fuzzycomp.nysiis("KNUTH")
    'NNAT'
    >>> fuzzycomp.nysiis("PHILLIPSON", False)
    'FFALAPSAN'
    >>> fuzzycomp.metaphone( "ANASTHA" )
    'ANS0'
    >>> fuzzycomp.metaphone("ESCARMANT", 7)
    'ESKRMNT'
    >>> fuzzycomp.cologne_phonetic("Breschnew")
    '17863'