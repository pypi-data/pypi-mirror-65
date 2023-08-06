import setuptools  # noqa

with open("README.md", "r") as fh:
    long_description = fh.read()
    description = long_description.split('\n')[0].replace('# ', '')

setuptools.setup(
    name="smarsy",
    version="0.0.10",
    author="KulZu",
    author_email="dkultasev@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkultasev/smarsy-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
)
