#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

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


class Test_chibi_hybrid( unittest.TestCase ):
    def test_should_work( self ):
        result = Dump.foo()
        self.assertIsInstance( result, Dump )
        self.assertEqual( 'cls', result.value )
        self.assertEqual( 'cls', result.foo() )

        result = Dump( 'cosa' ).foo()
        self.assertEqual( 'cosa', result )

    def test_should_work_the_property_class( self ):
        self.assertEqual( Dump.bar, '' )
        Dump.bar = "cosa 2"
        self.assertEqual( Dump.bar, 'cosa 2' )
