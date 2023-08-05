import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apigee-ci-tool",
    version="0.0.1",
    author="Ricardo Santamaria",
    author_email="ricardo.santamariah@gmail.com",
    description="A module with tools to make Apigee CICD easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GingRick/apigee-ci-tool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)