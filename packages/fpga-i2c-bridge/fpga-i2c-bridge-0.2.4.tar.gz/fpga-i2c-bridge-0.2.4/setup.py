import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='fpga-i2c-bridge',
    version='0.2.4',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='Hannes Preiss',
    author_email='sophie@sophieware.net',
    description='A library for managing and remotely controlling devices connected to one or several bridges, which in '
                'turn are communicated with via a specialized I2C protocol. Belongs to the FPGA Smart Home project.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=["smbus2>=0.3"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix"
    ]
)
