import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snowhut", # Replace with your own username
    version="0.2.0-beta",
    author="Jon McCarble",
    author_email="jon.mccarble@yum.com",
    description="A small package that simplifies connection to Pizza Hut's internal snowflake environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pizzahutdigital/snowflake_ph",
    download_url="https://github.com/pizzahutdigital/snowflake_ph/dist/snowhut-0.2.0b0.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "snowflake-connector-python"
    ]
)