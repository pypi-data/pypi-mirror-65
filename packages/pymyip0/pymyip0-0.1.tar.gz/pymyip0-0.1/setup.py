from setuptools import setup

setup(name='pymyip0',
      version='0.1',
      description=
      "Module for python 3.x to find out your ip, city, country.\n" +
      '\n' +
      'Use:\n' + 
      'import pymyip\n' +
      '\n' +
      'print("Your ip " + pymyip.get_ip())\n' +
      '\n' +
      'print("Your city " + pymyip.get_city())\n' +
      '\n' +
      'print("Your country" + pymyip.get_country())\n',
      py_modules=['pymyip'],
      author_email='illya.vosiychuk@gmail.com',
      zip_safe=False)