# pylint: disable=missing-docstring
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="portfolio-report-Sealeon",
    version="1.0.4",
    author="Emily Knight",
    author_email="emily.knight2@mohawkcollege.ca",
    description="A stock report generator",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/sheridan-python/assignment-7-Sealeon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "portfolio_report=portfolio.portfolio_report:main",
        ],
    },
)
