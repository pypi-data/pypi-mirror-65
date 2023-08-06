import setuptools

from fpga_device_manager.Constants import APP_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fpga-device-manager',
    version=APP_VERSION,
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='Hannes Preiss',
    author_email='sophie@sophieware.net',
    description='A GUI for managing FPGA Device configurations.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=['moody-templates', 'PySide2', 'QtPy'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)