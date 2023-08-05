import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdutilpy",
    version="0.0.1",
    author="Girish Dubey",
    author_email="dubey.girish2@gmail.com",
    description="A util package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/girishdubey/gdutilpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)