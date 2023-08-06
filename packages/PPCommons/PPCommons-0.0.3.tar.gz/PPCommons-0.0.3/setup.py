from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        readme_string = f.read()
    return readme_string


def get_required_packages():
    with open('requirements.txt', 'r') as f:
        required = f.read().splitlines()
    return required


setup(
    name="PPCommons",
    version="0.0.3",
    description="A Python3 package to rapidly setup server-less applications for AWS Lambda with generic features",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Arpit Gaur",
    author_email="dev.arpitgaur@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["ppcommons"],
    include_package_data=True,
    install_requires=get_required_packages(),
    entry_points={
        "console_scripts": [
            "ppcommons=ppcommons.cli:main",
        ]
    },
)