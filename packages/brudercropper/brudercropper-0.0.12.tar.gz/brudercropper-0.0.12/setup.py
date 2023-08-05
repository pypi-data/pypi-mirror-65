import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brudercropper", # Replace with your own username
    version="0.0.12",
    author="Niggo",
    # author_email="niggo@420.bayern",
    description="Croppt Zeug auf 62mm für Bruderlabeldrucker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://",
    packages=setuptools.find_packages(),
    classifiers=[
        # "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'brudercrop = brudercropper:brudercropper',
        ],
    }
)