import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="celery-worker",
    version='0.0.2',
    author="Anthony K GROSS",
    author_email="anthony.k.gross@gmail.com",
    description="A Simple celery worker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthonykgross/celery-worker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "celery>=4.3.0"
    ]
)
