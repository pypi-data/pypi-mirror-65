import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frodokem_with_chat",
    version="1.0.4",
    author="0xCA7",
    author_email="samselprzemyslaw@gmail.com",
    description="FrodoKEM implementation and presentation application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrzemyslawSamsel/AgainstQuantum",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pycryptodome', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)