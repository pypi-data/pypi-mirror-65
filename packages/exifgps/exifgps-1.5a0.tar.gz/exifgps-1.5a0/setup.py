#!/usr/bin/python3
#---------------------------------------------
# Script:   
# Name:     Javier
# Date:        Wed Sep 14 15:40:56 BST 2016
# Description:  
#---------------------------------------------

from setuptools import setup

setup(name="exifgps",
      version='v1.05-alpha',
      description="EXIF GPS information to Google Maps url",
      url="http://github.com/quincymd/exifgps",
      download_url="https://github.com/quincymd/exifgps/archive/v1.05-alpha.tar.gz",
      author="Cambell Spong",
      author_email="quincymd@mail.com",
      license="CC",
      packages=["exifgps"],
      install_requires=["exifread"],
      zip_safe=False)


