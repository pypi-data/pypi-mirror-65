from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.beaker'
version = '0.3'
readme = open(join('src', 'dolmen', 'beaker', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'beaker',
    'grokcore.component',
    'setuptools',
    'zope.component',
    'zope.interface',
    'zope.publisher',
    'zope.schema',
    'zope.session',
    'zope.site',
    'zope.traversing',
    ]

test_requires = [
    'pyhamcrest',
    'zope.component',
    'zope.event',
    'zope.i18n',
    'zope.principalregistry',
    'zope.security',
    'zope.securitypolicy',
    'zope.site',
    'zope.testing',
    ]


setup(name=name,
      version=version,
      description="An implementation of a zope session, using beaker.",
      long_description=readme + '\n' + history,
      keywords='Zope3 Session, Grok Dolmen',
      author='Souheil Chelfouh',
      author_email='',
      url='http://www.dolmen-project.org',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen',],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      extras_require={'test': test_requires},
      install_requires=install_requires,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
      )
