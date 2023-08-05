import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edge_st_sdk_package",
    version="1.0.27",
    author="Davide Aliprandi",
    author_email="davide.aliprandi@gmail.com",
    description="IoT edge computing abstraction library package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/STMicroelectronics/EdgeSTSDK_Python",
    packages=setuptools.find_packages(),
    license='BSD 3-clause',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Embedded Systems"
    ],
)
