
from setuptools import setup

setup(name='apminsight',
      version='1.0.0',
      description='application performance monitoring',
      url='https://site24x7.com',
      author='apm-insight',
      author_email='apm-insight@zohocorp.com',
      license='MIT',
      packages=['apminsight'],
      python_requires='>=3.5',
      install_requires=[
            "requests"
      ],
      zip_safe=False)