from setuptools import setup, find_packages

setup(
    name="os_scheduling_simulator",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description="OS Scheduling Simulator for COMP3320 Final Project",
    author="Shardia Gregory, Varyl Browne, Qadash Charles, Kemier Franics",
    author_email="500001139@my.fiveislands.uwi.edu ",
    python_requires=">=3.6",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "pandas>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)