import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brudercropper",
    version="0.1.5",
    author="Niggo",
    description="Croppt Zeug auf 62mm für Bruderlabeldrucker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "imutils==0.5.3",
        "numpy==1.18.2",
        "opencv-python==4.2.0.34",
        "Pillow==7.1.1",
        "pytesseract==0.3.3",
        "python-barcode==0.11.0"
    ],
    classifiers=[
        # "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'brudercrop = brudercropper.crop:main',
        ],
    }
)