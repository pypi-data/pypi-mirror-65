import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powerfuldeveloper-json-walker",  # Replace with your own username
    version="0.0.2",
    author="Powerfuldevleoper",
    author_email="apowerfuldeveloper@gmail.com",
    description="Walk on jsons like nothing :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/powerfuldeveloper/json_walker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
