import setuptools

print(setuptools.find_packages())

setuptools.setup(
    name="cloudwright_airtable",
    version="0.0.0-1",
    author="cloudwright",
    url="https://cloudwright.io",
    author_email="founders@cloudwright.io",
    description="cloudwright_airtable",
    packages=setuptools.find_packages(),
    install_requires=[ ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
