from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f_:
    long_description = f_.read()

def main():
    setup(name='kpsh',
          description="Rofi KeePass interface",
          long_description=long_description,
          long_description_content_type='text/markdown',
          use_scm_version={'write_to': 'src/kpd/_version.py'},
          license='GPLv3+',
          author='Michał Góral',
          author_email='dev@mgoral.org',
          url='https://gitlab.com/mgoral/kpsh',
          platforms=['linux'],
          python_requires='>=3.7,<3.8',
          setup_requires=['setuptools_scm'],
          install_requires=[
              'pykeepass==3.2.0',
              'prompt_toolkit==2.0.9',
          ],

          # https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=['Development Status :: 4 - Beta',
                       'Environment :: Console',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3 :: Only',
                       'Programming Language :: Python :: 3.7',
                       'Topic :: Utilities',
                       ],

          packages=find_packages('src'),
          package_dir={'': 'src'},

          entry_points={
              'console_scripts': ['kpsh=kpd.app:main'],
          },
          scripts=['contrib/kpsh-menu', 'contrib/kpsh-client'])

if __name__ == '__main__':
    main()
