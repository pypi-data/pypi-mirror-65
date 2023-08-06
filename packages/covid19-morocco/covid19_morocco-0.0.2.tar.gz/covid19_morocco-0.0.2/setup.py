import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid19_morocco", # Replace with your own username
    version="0.0.2",
    author="Ballouch",
    author_email="mohamedballouch10@gmail.com",
    description="A Python Package to get covid19 Cases for Morocco in Real Time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mohamedballouch/",
    packages=["covid19_morocco"],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)