import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deewr-tga-course-extract",
    version="0.0.1",
    author="Kieran McDougall",
    author_email="kieran@fromz.com.au",
    description="Extract course content from training.gov.au",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fromz/deewr-tga",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)