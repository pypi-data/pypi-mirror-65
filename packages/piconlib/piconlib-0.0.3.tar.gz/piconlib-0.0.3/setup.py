import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piconlib", # Replace with your own username
    version="0.0.3",
    author="Tau5",
    author_email="tau0@tutanota.com",
    description="A library to interact with Picon's system tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tau5/piconlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)