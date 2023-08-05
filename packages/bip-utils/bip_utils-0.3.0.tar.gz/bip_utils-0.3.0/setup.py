import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bip_utils",
    version="0.3.0",
    author="Emanuele Bellocchia",
    author_email="ebellocchia@gmail.com",
    description="Implementation of BIP39, BIP32, BIP44, BIP49 and BIP84 for wallet seeds, keys and addresses generation. Supported coins: Bitcoin, Litecoin, Dogecoin, Ethereum.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebellocchia/bip_utils",
    download_url="https://github.com/ebellocchia/bip_utils/archive/v0.3.0.tar.gz",
    license="MIT",
    test_suite="tests",
    install_requires = ["ecdsa","pysha3"],
    packages=["bip_utils"],
    package_data={"bip_utils": ["bip39_wordslist_en.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
