from setuptools import setup, find_packages

setup(
    name="rshanker779_common",
    version="0.0.9",
    author="rshanker779",
    author_email="rshanker779@gmail.com",
    description="Common utilities",
    python_requires=">=3.7",
    install_requires=[
        "black",
        "bump2version>=1.0.0",
        "pre-commit~=2.2",
        "pytest>5.4,<6",
        "pytest-cov~=2.8",
        "requests<3",
        "snakeviz",
        "wheel>0.33",
    ],
    packages=find_packages(),
    extras_require={"docs": ["sphinx"]},
)
