import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gorani", # Replace with your own username
    version="1.0.2",
    author="Sunho Kim",
    author_email="ksunhokim123@naver.com",
    description="Gorani Reader data pipeline utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6'
)