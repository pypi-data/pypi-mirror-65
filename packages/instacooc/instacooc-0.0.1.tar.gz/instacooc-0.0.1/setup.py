from setuptools import setup

setup(
name='instacooc',
version='0.0.1',
author='Meysam Kheyrollah',
author_email='meysamkheyrollahnejad@gmail.com',
install_requires=[
   'pymysql',
   'pandas'
],
py_modules=["instacooc","storage"],
package_dir={'': "module"},
package_data={'': "module/src/*"},
)
