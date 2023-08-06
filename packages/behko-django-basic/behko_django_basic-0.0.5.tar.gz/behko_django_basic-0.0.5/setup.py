import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="behko_django_basic", # Replace with your own username
    version="0.0.5",
    author="powerfuldeveloper",
    author_email="apowerfuldeveloper@gmail.com",
    description="Makes it easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/powerfuldeveloper/cool_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)