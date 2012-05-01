
# -*- coding: utf-8 -*-
"""
This module contains the osha.theme package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.4.17dev'

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
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        ],
      keywords='osha plone theme webcouturier',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='https://svn.syslab.com/svn/OSHA/osha.theme',
      license='GPL + EUPL',
      packages = ['osha', 'osha/theme'],
      package_dir = {'' : 'src'},
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CallForContractors',
          'Products.CaseStudy',
          'Products.DataGridField',
          'Products.LinguaPlone',
          'Products.OSHContentLink',
          'Products.PressRoom',
          'Products.PublicJobVacancy',
          'Products.QueueCatalog',
          'Products.RALink',
          'Products.RemoteProvider',
          'Products.RichDocument',
          'Products.TextIndexNG3',
          'Products.Collage',
          'collective.captcha',
          'dateable.chronos',
          'ordereddict',
          'osha.adaptation',
          'osha.policy',
          'osha.translations',
          'osha.whoswho',
          'p4a.subtyper',
          'plone.app.blob',
          'plone.memoize',
          'python_memcached',
          'slc.alertservice',
          'slc.autotranslate',
          'slc.googlesearch',
          'slc.linguatools',
          'slc.publications',
          'slc.shoppinglist',
          'slc.subsite',
          'slc.xliff',
          'z3c.jbot',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

