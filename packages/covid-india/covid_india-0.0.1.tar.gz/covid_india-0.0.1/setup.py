import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid_india",
    version="0.0.1",
    author="Debdut Goswami",
    author_email="debdutgoswami@gmail.com",
    description="A package to provide information regarding COVID-19 cases in India.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debdutgoswami/covid-india",
    download_url = 'https://github.com/debdutgoswami/covid-india/archive/v_0.0.1.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)