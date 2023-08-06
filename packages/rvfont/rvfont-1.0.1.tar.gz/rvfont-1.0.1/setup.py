import setuptools
with open('README.md','r') as fh:
    long_description = fh.read()
setuptools.setup(
    name = "rvfont",
    version = '1.0.1',
    author="Ravikirana B",
    author_email="ravikiranb36@gmail.com",
    description="Fontchooser for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravikiranb36/rvfont.git",
    license="MIT",
    packages=["rvfont"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8' ,
)