import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="hue_cli",
    version="0.1.0",
    author="Matt Boran",
    author_email="mattboran@gmail.com",
    description="A script to be run from Xcode to lint files as you make changes",
    long_description="To come",
    long_description_content_type="text/markdown",
    url="https://github.com/mattboran/hue-cli",
    download_url="https://github.com/mattboran/hue-cli/releases/download/0.1.0/hue_cli-0.1.0-py3-none-any.whl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'requests>=2.23.0',
        'webcolors>=1.11'
    ],
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'hue = cli:main'
        ]
    }
)
