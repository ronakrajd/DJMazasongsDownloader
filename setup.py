from setuptools import setup, find_packages

setup(
    name='DJMazasongsLinkGrabber',
    version='1.0',
    packages=find_packages(),
    package_data={
        'DJMazasongsLinkGrabber': ['*.json']},
    entry_points={
        'scrapy': ['settings = DJMazasongsLinkGrabber.settings']
    })