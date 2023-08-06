============
chibi_hybrid
============


.. image:: https://img.shields.io/pypi/v/chibi_hybrid.svg
        :target: https://pypi.python.org/pypi/chibi_hybrid

.. image:: https://img.shields.io/travis/dem4ply/chibi_hybrid.svg
        :target: https://travis-ci.org/dem4ply/chibi_hybrid

.. image:: https://readthedocs.org/projects/chibi-hybrid/badge/?version=latest
        :target: https://chibi-hybrid.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




simple class for have hybrid class and instance methods
and add class properties


* Free software: WTFPL
* Documentation: https://chibi-hybrid.readthedocs.io.


Features
--------


.. code-block:: python

	from chibi_hybrid.chibi_hybrid import Chibi_hybrid, Class_property


	class Dump:
		__bar = ''

		def __init__( self, value ):
			self.value = value

		@Chibi_hybrid
		def foo( cls ):
			return cls( 'cls' )

		@foo.instancemethod
		def foo( self ):
			return self.value

		@Class_property
		def bar( cls ):
			return cls.__bar

		@bar.setter
		def bar( cls, value ):
			cls.__bar = value

	result = Dump.foo()
	assert result == Dump
	assert 'cls' == result.value
	assert 'cls' == result.foo()

	result = Dump( 'cosa' ).foo()
	assert 'cosa' == result

	assert Dump.bar == ''
	Dump.bar = "cosa 2"
	assert Dump.bar == 'cosa 2'
