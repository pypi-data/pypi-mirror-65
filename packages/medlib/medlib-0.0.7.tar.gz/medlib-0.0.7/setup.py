from setuptools import setup, find_packages
from medlib.setup.setup import getSetupIni

sp=getSetupIni()

setup(
      name=sp['name'],
      version=sp['version'],
      description='Media Library: Media Manager',
      long_description="Media Manager",	#=open('README.md', encoding="utf-8").read(),
      url='http://github.com/dallaszkorben/medlib',
      author='dallaszkorben',
      author_email='dallaszkorben@gmail.com',
      license='MIT',
      classifiers =[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
      ],
      packages = find_packages(),
      setup_requires=[ "pyqt5", "pyqt5-sip", "numpy", 'configparser', 'psutil'],
      install_requires=["pyqt5", 'pyqt5-sip', 'numpy', 'configparser', 'psutil'],
      entry_points = {
        'console_scripts': [
		'medlib=medlib.gui.medlib_gui:main'
		]
      },
      package_data={
        'cardholder': ['img/*.gif'],
        'medlib': ['gui/images/*.png'],
        'medlib': ['mediamodel/images/*.png'],
        'medlib': ['setup/setup.ini'],
        'medlib': ['dict/*.properties']
      },
      include_package_data = True,
      zip_safe=False)
