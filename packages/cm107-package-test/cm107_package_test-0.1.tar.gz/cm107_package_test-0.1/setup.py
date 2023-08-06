from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cm107_package_test',
    version='0.1',
    description="packaging test of cm107",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cm107/cm107_package_test",
    author='Clayton Mork',
    author_email='mork.clayton3@gmail.com',
    license='MIT License',
    packages=find_packages(
        where='.',
        include=['cm107_package_test*']
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'opencv-python>=4.1.1.26',
        'numpy>=1.17.2',
        'pylint>=2.4.2'
    ],
    python_requires='>=3.6'
)
