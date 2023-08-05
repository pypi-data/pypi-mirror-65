import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulseapi_integration_calibrate",
    version="0.0.2",
    author="Matskevich",
    author_email="matskevichivan98@gmail.com",
    description="Calibrate plane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Matskevichivan/Calibrate",
    packages=["pulseapi_integration_calibrate"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pulseapi>=1.6',
                      'numpy>=1.18',
                      'pulseapi_integration>=0.1.0']
)
