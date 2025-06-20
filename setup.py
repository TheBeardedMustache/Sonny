from setuptools import setup, find_packages

setup(
    name="sonny",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    # Dependencies are managed via requirements.txt
    install_requires=[],
    description="Sonny: Integrated agent platform",
    author="Sonny Team",
    author_email="sonny@example.com",
)