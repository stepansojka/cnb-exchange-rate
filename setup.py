import glob
from distutils.core import setup

setup(
    name = "cnb-exchange-rate",
    packages = ["cnb_exchange_rate"],
    version = "0.0.0",
    description = "Czech National Bank Exchange Rate Downloader",
    author = "Stepan Sojka",
    author_email = "stepansojka@countermail.com",
    url = "http://github.com/stepansojka/cnb-exchange-rate",
    keywords = ["www"],
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        ],
    long_description = """\
Czech National Bank Exchange Rate Downloader
-------------------------------------

TBD
"""
)
