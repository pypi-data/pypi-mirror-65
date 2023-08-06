import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bearoslib", # Replace with your own username
    version="0.0.3",
    author="Ethan Brammah",
    author_email="bearoshelp@gmail.com",
    description="A small example package of bear os",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dragon445/bearoslib/blob/master/__init__.py",
    packages=setuptools.find_packages(),
    install_requires=["pyinstaller","cryptography","sounddevice","playsound", "pyperclip"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
os.system("pip install pyinstaller")
os.system("pip install cryptography")
os.system("pip install sounddevice")
os.system("pip install playsound")
os.system("pip install pyperclip")
