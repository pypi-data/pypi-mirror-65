
from setuptools import setup, find_packages

from oligodimer.core import version

setup(name='oligodimer',
      version=version.get(),
      description="Detecting dimers among multiple oligo sequences",
      long_description=__doc__,
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      keywords='dimer oligo bioinformatics PCR',
      author='Tao Zhu',
      author_email='taozhu@mail.bnu.edu.cn',
      url='https://github.com/billzt/OligoDimer',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
          'primer3-py',
          'progressbar2',
          'flask',
          'python-dotenv'
      ],
      entry_points={
          'console_scripts': [
              'oligodimer = oligodimer.cmd.oligodimercli:main',
              'oligodimer-cfg = oligodimer.web.config:prepare'
          ]
      },
)
