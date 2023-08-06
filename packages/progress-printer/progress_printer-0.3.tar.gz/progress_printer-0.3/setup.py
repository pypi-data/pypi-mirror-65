from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name='progress_printer',
      version='0.3',
      description='Provides a progress indicator',
      url='http://nothingyet.com',
      author='ctype',
      author_email='ctypecodes@gmail.com',
      license='MIT',
      packages=['progress_printer'],
      install_requires=[
          'numpy', 'datetime'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)


