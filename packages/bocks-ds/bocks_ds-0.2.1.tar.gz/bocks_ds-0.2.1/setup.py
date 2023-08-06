import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bocks_ds",
    version="0.2.1",
    author="Bocks",
    description="DataSource Python SDK",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/bocks-ds/datasource-python",
    packages=setuptools.find_packages(),
    install_requires=[
            'pycurl'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
