import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turbo_dash",
    version="0.1.1",
    author="turbo3136",
    author_email="turbo3136@gmail.com",
    description="automated Dash framework with templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turbo3136/turbo_dash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'dash>=1.8.0',
        'dash-core-components>=1.7.0',
        'dash-html-components>=1.0.2',
        'plotly>=4.0.0',
    ],
)
