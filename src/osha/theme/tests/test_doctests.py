import doctest
import unittest

from base import OshaThemeFunctionalTestCase

from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    return unittest.TestSuite((

            Suite('tests/mytest.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.theme',
                   test_class=OshaThemeFunctionalTestCase) ,

            Suite('tests/oshnetwork_member_view.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.theme',
                   test_class=OshaThemeFunctionalTestCase) ,

        ))
