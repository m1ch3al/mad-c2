"""
A setuptools based on setup module for MADIS.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="m1ch3al-autonomous-drone-internal-system",
    version="0.1",
    description="The MAD internal system (run into raspberry pi).",
    # The project's main homepage.
    url="https://github.com/m1ch3al/madis.git",
    # Author details
    author="Renato Sirola",
    author_email="renato.sirola@gmail.com",
    # Choose your license
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # What does your project relate to?
    keywords="sensors ros hardware drone autonomy",
    include_package_data=False,
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'PyYAML',
        'pyserial',
        'gps',
        'rospkg',
    ],
    packages=[
        'madis',
        'madis.utils',
        'madis.ros',
        'madis.sensors',
        'madis.tests',
    ]
)

