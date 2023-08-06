import setuptools

with open("Polygott/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Polygott", # Replace with your own username
    version="0.0.1",
    author="Repl.it User",
    author_email="xsumagravity@gmail.com",
    description="run polygott in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repl.it/@Downey/Polygott-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.6',
)