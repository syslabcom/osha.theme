# -*- coding: utf-8 -*-
"""
This module contains the osha.theme package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.2.21'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'osha', 'theme', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' 
    )
    
tests_require=['zope.testing']

setup(name='osha.theme',
      version=version,
      description="Plone theme for OSHA web site",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='osha plone theme webcouturier',
      author='Denis Mishunov',
      author_email='denis@webcouturier.com',
      url='http://www.webcouturier.com',
      license='GPL',
      packages = ['osha', 'osha/theme'],
      package_dir = {'' : 'src'},
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.subtyper',
          'p4a.calendar',
          'p4a.fileimage',
          'dateable.chronos',
          'Products.collage',
          'Products.OSHContentLink',
          'Products.VocabularyPickerWidget',
          'slc.publications',
          'slc.shoppinglist',
          'Products.PressRoom',
          'slc.subsite',
          'osha.policy',
          'Products.OSHATranslations',
          'Products.LinguaPlone',
          'slc.linguatools',
          'Products.DataGridField',
          'slc.clicksearch',
          'Products.RemoteProvider',
          'Products.RALink',
          'Products.CaseStudy',
          'Products.RichDocument',
          'osha.whoswho',
          'plone.app.blob',
          'plone.memoize',
          'python_memcached',
          'Products.CallForContractors',
          'Products.PublicJobVacancy',
          'Products.RiskAssessmentLink',
          'simplon.plone.ldap',
          'Products.QueueCatalog',
          'slc.autotranslate',
          'Products.FCKEditor',
          'Products.TextIndexNG3',
          'Products.LinguaPlone',
          'collective.captcha',
          'collective.lead',
          'slc.xliff',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'osha.theme.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      """,
      paster_plugins = ["ZopeSkel"],
      )      
      
