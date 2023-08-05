import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="gwx-telehealth",
    version="0.0.6",
    author="Jerric Calosor",
    author_email="jerric.calosor@groworx.com.au",
    description="Adapter for telehealth systems API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'gwx_telehealth': ['config/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
