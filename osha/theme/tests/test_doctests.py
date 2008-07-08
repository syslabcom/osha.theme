import os, sys

import glob
import doctest
import unittest
from Globals import package_home
from base import OshaThemeFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite


OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return unittest.TestSuite((

            Suite('tests/linguatest.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.theme',
                   test_class=OshaThemeFunctionalTestCase) ,

            Suite('tests/mytest.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.theme',
                   test_class=OshaThemeFunctionalTestCase) ,

            Suite('tests/dbfilter.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.theme',
                   test_class=OshaThemeFunctionalTestCase) ,


        ))
