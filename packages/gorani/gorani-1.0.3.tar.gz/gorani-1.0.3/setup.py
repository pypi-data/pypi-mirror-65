import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gorani", # Replace with your own username
    version="1.0.3",
    author="Sunho Kim",
    author_email="ksunhokim123@naver.com",
    description="Gorani Reader data pipeline utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=[
        'ebookli>=0.17.1',
        'inscriptis>=1.0',
        'lxml>=4.5.0',
        'nltk>=3.4.5',
        'numpy>=1.11',
        'pandas>=1.0.3',
        'python-dateutil>=2.8.1'
    ]
)