
About
=====
*Fuzzycomp* is a package purely implemented in Python for comparing
sequences or strings. Some algorithms work equally well on strings as on any
iterable and some algorithms are only for string comparison.

Platforms
=========
*Fuzzycomp* has been tested to work with the following versions of python.
  * Python 2.4
  * Python 2.5
  * Python 2.6
  * Python 2.7

Algorithms
==========
*Fuzzycomp* implements the following algorithms.

Comparison
----------
  * `Levenshtein Distance <https://secure.wikimedia.org/wikipedia/en/wiki/Levenshtein_distance>`__
  * `JaccardDistance <https://secure.wikimedia.org/wikipedia/en/wiki/Jaccard_index>`__
  * `Hamming Distance <https://secure.wikimedia.org/wikipedia/en/wiki/Hamming_distance>`__
  * `Jaro Distance <https://secure.wikimedia.org/wikipedia/en/wiki/Jaro%E2%80%93Winkler_distance>`__
  * `Jaro Winkler Distance <https://secure.wikimedia.org/wikipedia/en/wiki/Jaro%E2%80%93Winkler_distance>`__
  * `Dice Coefficient <https://secure.wikimedia.org/wikipedia/en/wiki/Dice%27s_coefficient>`__
  * `Longest common subsequence <https://secure.wikimedia.org/wikipedia/en/wiki/Longest_common_subsequence_problem>`__

Phonetic
--------
  * `American Soundex <https://secure.wikimedia.org/wikipedia/en/wiki/Soundex>`__
  * `New York State Identification and Intelligence System ( NYSIIS ) <http://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System>`__
  * `Metaphone <http://aspell.net/metaphone/metaphone-kuhn.txt>`__
  * `Cologne Phonetic (Kölner Phonetik) <http://commons.apache.org/codec/apidocs/org/apache/commons/codec/language/ColognePhonetic.html>`__

Background
==========
There several major reasons for developing and publishing *fuzzycomp*
although there are other packages available, implementing most of the
algorithms present in *fuzzycomp*.

  #. There are an astonishing amount of different ways available for
     classifying how similar two strings are, once you leave the domain of
     perfect matching. It started with me, needing a way to tell how well a
     search phrase was matching the results provided by an external API. Once I
     started searching, I was really amazed by the subject and by the many
     alternatives there were so I wanted to learn more by developing the
     algorithms in Python.
  #. This is my first Python packages developed with the intent to be
     distributed and used by others. I wanted to learn how to structure and
     develop a Python package that could be released to the public and that
     could be useful in some way.
  #. The last couple of years I have read more and more about unit-testing
     and test driven development (TDD), almost always positive things. I have
     not had the opportunity to use unit-tests in any previous projects,
     so this is my learning ground for TDD and writing unit-tests.

Install
=======
The package is not yet represented on PyPI so the best ways to install
*fuzzycomp* at the moment are:

Using *pip* replacing X Y Z for the version number that you want to install::

 pip install http://fuzzycomp.googlecode.com/files/fuzzycomp-X.Y.Z.tar.gz

Or by downloading and unpacking the desired version and from the console
executing::

 python setup.py install


Usage
=====
Some example usage of *fuzzycomp*::

 >>> from fuzzycomp import fuzzycomp
 >>> fuzzycomp.levenshtein_distance( "Hello", "world" )
 3

 >>> fuzzycomp.soundex("Alfred")
 'A416'

Alternatives
============
If speed is of utmost importance to you or you find yourself comparing very
long sequences, you should probably consider some of the available
alternatives out there. They implement most of the algorithms in C so should
be considerably faster.

Some, but by no means all, alternatives are:
  * `python-Levenshtein <http://pypi.python.org/pypi/python-Levenshtein/0.10.2>`__

  * `Fuzzy <http://pypi.python.org/pypi/Fuzzy/1.0>`__

  * `jellyfish <http://pypi.python.org/pypi/jellyfish/0.1.2>`__

Contact
=======
For bugs or feature requests, please use the issue tracker on the project page.

To get in contact with me regarding the project,
please email fuzzycomp@googlegroups.com or follow me on twitter
`@fuzzycode <https://twitter.com/#!/fuzzycode>`__.