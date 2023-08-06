from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f_:
    long_description = f_.read()


def main():
    setup(name='webarchive',
          description="Archive web articles",
          long_description=long_description,
          long_description_content_type='text/markdown',
          use_scm_version={'write_to': 'src/wa/_version.py'},
          license='GPLv3+',
          author='Michał Góral',
          author_email='dev@goral.net.pl',
          url='https://gitlab.com/mgoral/webarchive',
          platforms=['linux'],
          python_requires='>=3.7,<3.9',
          setup_requires=['setuptools_scm'],
          install_requires=[
              'requests==2.23.0',
              'beautifulsoup4==4.8.2',
              'readability-lxml==0.7.1',
              'lxml==4.5.0',
              'chardet==3.0.4',
          ],
          extras_require={
              'gui': ['PyQt5'],
          },

          # https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=['Development Status :: 4 - Beta',
                       'Environment :: Console',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3 :: Only',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Topic :: Utilities',
                       ],

          packages=find_packages('src'),
          package_dir={'': 'src'},

          entry_points={
              'console_scripts': ['webarchive=wa.app:main'],
          },
          scripts=['contrib/webarchive-qt'])


if __name__ == '__main__':
    main()
