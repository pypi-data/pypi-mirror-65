import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heppdap",
    version="0.0.1",
    author="Brandon Weindorf",
    author_email="bjweindorf@gmail.com",
    description="High Energy Particle Physics Data Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bweindorf/HEPPDAP.git",
    install_requires=["matplotlib", "scipy", "numpy"],
    entry_points={
        "console_scripts": [
            "heppdap=scripts.main:main",
            ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
