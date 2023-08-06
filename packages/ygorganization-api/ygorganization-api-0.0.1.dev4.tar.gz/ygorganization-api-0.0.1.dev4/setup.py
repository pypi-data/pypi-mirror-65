import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ygorganization-api",
    version="0.0.1.dev4",
    author="gallantron",
    author_email="treeston.mmoc@gmail.com",
    description="Efficient querying of db.ygorganization.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://db.ygorganization.com/about/api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)