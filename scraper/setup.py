from setuptools import setup

setup(
    name="scraper",
    version="0.1",
    description="Module for scraping adverts from heyjobs",
    author="Joshua Greenhalgh",
    packages=["scraper"],
    zip_safe=False,
    entry_points={"console_scripts": ["run=scraper.run:main"]},
)
