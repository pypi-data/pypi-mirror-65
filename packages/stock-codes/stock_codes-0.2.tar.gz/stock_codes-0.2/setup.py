from setuptools import setup

setup(name='stock_codes',
      version='0.2',
      description='Analyze excel files to get codes',
      url='https://github.com/Fedex75/stock_codes',
      author='Federico Meza',
      author_email='mezafabrello@gmail.com',
      license='MIT',
      packages=['stock_codes'],
      install_requires=[
        'pandas',
        'xlrd',
        'openpyxl'
      ],
      zip_safe=False)
