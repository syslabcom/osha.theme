from setuptools import setup, find_packages

version = '0.1'

setup(name='osha.theme',
      version=version,
      description="Plone theme for OSHA web site",
      long_description="""\
""",
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
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
