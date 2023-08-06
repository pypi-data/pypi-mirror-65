import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portfolio-report-Sealeon",
    version="1.0",
    author="Emily Knight",
    author_email="emily.knight2@mohawkcollege.ca",
    description="A stock report generator",
    long_description=long_description,
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
)
