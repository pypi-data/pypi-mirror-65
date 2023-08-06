import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sauce_finder",
    version="2.2.0",
    author="Miika Launiainen",
    author_email="miika.launiainen@gmail.com",
    description="Script to find and download anime images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/miicat/sauce-finder",
    scripts=['sauce_finder/sauce_finder'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.0',
    install_requires=[
        'click',
        'validators',
        'requests'
    ]
)
