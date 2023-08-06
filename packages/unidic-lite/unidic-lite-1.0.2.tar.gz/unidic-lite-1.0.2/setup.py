import pathlib
import setuptools
from distutils.core import setup

setup(name='unidic-lite', 
      version='1.0.2',
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="A small version of UniDic packaged for Python",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/unidic-lite",
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Japanese",
      ],
      package_data={'unidic_lite': ['dicdir/*']}
      )
