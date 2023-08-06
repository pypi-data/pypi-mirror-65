"""
Setup and installation for the package.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="kelly",
    version="1.0",
    url="http://gitlab.com/zachwill/kelly",
    author="Zach Williams",
    author_email="hey@zachwill.com",
    description="A Python module for working with the Kelly Criterion",
    keywords=["kelly", "odds", "kelly criterion", "zachwill"],
    packages=[
        "kelly"
    ],
    install_requires=[
        "numpy>=1.17",
        "pandas>=0.25",
    ],
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
    ],
)
