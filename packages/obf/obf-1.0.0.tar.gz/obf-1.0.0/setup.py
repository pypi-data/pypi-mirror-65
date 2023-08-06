import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open ("obf/VERSION", "r") as fh2:
    version = fh2.read()

setuptools.setup(
    name="obf",
    version=version,
    author="Hossein Ghodse",
    author_email="hossein.ghodse@gmail.com",
    description="an obfuscation tool and library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hossg/obf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['obf=obf.commandline:main']
    },
    # install_requires=[
    #       'demjson'
    # ]
)