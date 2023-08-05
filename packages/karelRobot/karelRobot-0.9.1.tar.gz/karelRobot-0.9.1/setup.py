#############################################
# File Name: setup.py
# Author: hbynlsl
# Mail: hbynlsl@hotmail.com
# Created Time:  2020-04-06
#############################################
from setuptools import setup, find_packages

setup(
    name="karelRobot",
    version="0.9.1",
    keywords="karel robot",
    description="karel for python",
    license="MIT Licence",
    url="https://github.com/hbynlsl/karelRobot",
    author="hbynlsl",
    author_email="hbynlsl@hotmail.com",
    include_package_data=True,
    packages=find_packages(),
    data_files=[('Lib/site-packages/karelRobot/icons', ['icons/edit.png', 'icons/new.png', 'icons/open.png', 'icons/play.png', 'icons/reload.png', 'icons/reset.png', 'icons/running.png', 'icons/save.png', 'icons/saveas.png', 'icons/settings.png', 'icons/stop.png'])],
    zip_safe=False
)
