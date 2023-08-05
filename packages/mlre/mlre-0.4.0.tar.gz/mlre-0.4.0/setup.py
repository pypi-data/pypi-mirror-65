from distutils import util

import setuptools

# Load version number from module
main_ns = {}
ver_path = util.convert_path('mlre/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# Get README directly
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlre",
    version=main_ns['__version__'],
    author="Clemens-Alexander Brust",
    author_email="cabrust@pm.me",
    description="Machine Learning Research Environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cabrust/mlre",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License"
    ],
    python_requires='>=3.7',
    install_requires=["requests==2.22.0", "Flask==1.1.1"]
)
