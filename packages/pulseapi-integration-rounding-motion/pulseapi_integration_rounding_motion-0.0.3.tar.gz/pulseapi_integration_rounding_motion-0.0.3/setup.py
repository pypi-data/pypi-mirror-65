import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulseapi_integration_rounding_motion",  # Replace with your own username
    version="0.0.3",
    author="Matskevich",
    author_email="matskevichivan98@gmail.com",
    description="Move robot with blends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Matskevichivan/Blend",
    packages=["pulseapi_integration_rounding_motion"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pulse-api>=1.6',
                      'numpy>=1.18',
                      'pulseapi_integration>=0.1.0']
)
