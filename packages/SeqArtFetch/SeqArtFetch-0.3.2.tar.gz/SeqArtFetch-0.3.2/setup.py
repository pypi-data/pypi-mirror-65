from setuptools import setup, find_packages
from main import VERSION

setup(
    name="SeqArtFetch",
    description="A near-universal webcomic/sequential art downloader.",
    author="deing",
    author_email="admin@15318.de",
    version=VERSION,
    license="MIT",
    url="https://github.com/deingithub/SeqArtFetch",
    packages=["."],
    zip_safe=True,
    install_requires=["aiohttp", "cssselect", "lxml"],
    entry_points={"console_scripts": ["sqf=main:totally_not_main"]},
    long_description="""
A near-universal webcomic/sequential art downloader.
It visits each page like a human user, scraping and downloading all art images into a specified folder and by default only re-downloads new episodes.

`Details and Usage on GitHub <https://github.com/deingithub/SeqArtFetch>`_
    """,
)
