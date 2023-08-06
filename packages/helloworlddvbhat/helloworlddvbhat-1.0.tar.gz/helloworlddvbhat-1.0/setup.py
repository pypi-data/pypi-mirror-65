
from setuptools import setup

setup(name='helloworlddvbhat',
      version='1.0',
      description='Package markdown hello tst',
      author='Bhat D',
      py_modules=["helloworld"],
      package_dir={'':'src'},
      install_requires=["blessings ~=1.7",'boto3','snowflake-connector-python'],
      extras_require = {
            "dev":["pytest>=3.7",]
          },
     )
