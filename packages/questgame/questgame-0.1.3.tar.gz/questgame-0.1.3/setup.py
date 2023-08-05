import setuptools
from pathlib import Path

setuptools.setup(
    name="questgame",
    version="0.1.3",
    author="Chris Proctor",
    author_email="chris@chrisproctor.net",
    description="A simple game framework",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/cproctor/quest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "arcade==2.3.8",
        "easing-functions>=1.0.3",
        "numpy>=1.17.4",
        "Pillow>=6.2.1",
        "tqdm>=4.42.1",
        "xvfbwrapper>=0.2.9",
    ]
)
