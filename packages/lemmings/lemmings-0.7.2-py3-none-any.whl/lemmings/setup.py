import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lemmings", 
    version="0.7.0",
    author="radiantgeek",
    author_email='',
    license='MIT',
    description="Async load testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/radiantgeek/lemmings",
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    install_requires=[
        "httpx>=0.11.1", 
        "prometheus_client>=0.7.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)