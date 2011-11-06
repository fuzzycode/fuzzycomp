Installing
==========

Dependencies
------------
The only dependency for **fuzzycomp** is python 2.4 - 2.7. No additional packages needs to be
installed.

Install
-------
Using *pip* replacing X Y Z for the version number that you want to install::

 pip install http://fuzzycomp.googlecode.com/files/fuzzycomp-X.Y.Z.tar.gz


Or by downloading and unpacking the desired version and from the consol executing::

    python setup.py install


Testing
-------
**Fuzzycomp** comes with a complete test suite included in the package. To run the test suite,
do the following::

 $ cd fuzzycomp/tests
 $ python test_fuzzycomp.py

And you should see something like this::

 Running tests
 Running tests2
 ...............................................................................
 ----------------------------------------------------------------------
 Ran 79 tests in 0.096s

 OK