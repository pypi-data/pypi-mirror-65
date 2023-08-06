from setuptools import setup

version = "1.1.0"

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as req_file:
    requirements = req_file.readlines()

setup(
    name="smort-query",
    version=version,
    description=("Django like query engine for any objects."),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Mateusz Nowak",
    author_email="nowak.mateusz@hotmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/matiuszka/smort-query",
    packages=["smort_query",],
    python_requires=">=3.6",
    package_dir={"smort_query": "smort_query"},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
)
