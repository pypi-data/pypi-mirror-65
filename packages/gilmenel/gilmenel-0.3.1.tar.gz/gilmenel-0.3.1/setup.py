import setuptools

import versioneer

# check to prevent dirty uploads to PyPI
if versioneer.get_versions()["dirty"]:

    class MustCommitError(Exception):
        pass

    raise MustCommitError("please commit everything before releasing")

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'astropy',
    'astroquery',
    'sqlalchemy',
    'matplotlib',
    'click',
    'tqdm',
]

test_requirements = ['pytest', 'pytest-cov', 'pytest-watch', 'pytest-reportlog']

setuptools.setup(
    author="SALT Software Engineers",
    author_email="salt-support@salt.ac.za",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    cmdclass=versioneer.get_cmdclass(),
    description="Telescope guide star selection tools.",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="gilmenel",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=test_requirements,
    url="https://bitbucket.org/saao/gilmenel",
    version=versioneer.get_version(),
)
