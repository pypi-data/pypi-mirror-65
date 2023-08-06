import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neon-goby", # Replace with your own username
    version="0.0.6",
    author="HiiYL",
    author_email="hii@saleswhale.com",
    description="A simple package to clean email bodies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=[
        'contractions==0.0.23',
        'email_reply_parser==0.5.9',
        'syntok==1.2.1',
        'beautifulsoup4==4.7.1'
    ],
    test_requires=[
        'pytest',
        'pytest-cov',
        'pylint'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
