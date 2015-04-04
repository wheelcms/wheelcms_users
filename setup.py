from setuptools import setup, find_packages
import os

version = '0.9'

setup(name='wheelcms_users',
      version=version,
      description="WheelCMS user management",
      long_description=open("README.md").read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ivo van der Wijk',
      author_email='wheelcms@in.m3r.nl',
      url='http://github.com/wheelcms/wheelcms_users',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'wheelcms_axle',
          'pytest',
          'mock',
      ],
      entry_points={
      },

      )

