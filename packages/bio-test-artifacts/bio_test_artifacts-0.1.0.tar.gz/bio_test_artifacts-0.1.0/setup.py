import os
from setuptools import setup, find_packages

version = "0.1.0"

# Description from README.md
base_dir = os.path.dirname(os.path.abspath(__file__))
long_description = "\n\n".join([open(os.path.join(base_dir, "README.md"), "r").read()])

setup(
    name="bio_test_artifacts",
    version=version,
    description="Test Artifacts for Biology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asistradition/bio-test-artifacts",
    author="Chris Jackson",
    author_email="cj59@nyu.edu",
    maintainer="Chris Jackson",
    maintainer_email="cj59@nyu.edu",
    packages=find_packages(include=["bio_test_artifacts", "bio_test_artifacts.*"]),
    package_data={'bio_test_artifacts': ['prebuilt/artifacts/*']},
    zip_safe=False,
    install_requires=["numpy", "pandas"],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ]
)
