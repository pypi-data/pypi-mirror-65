from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pysection",
    version="0.0.2",
    author="Cheng Lan",
    author_email="lan@bolinaingegneria.com",
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    install_requires=['shapely','numpy','pandas','xlrd','tables','matplotlib','plotly'],
    url='https://github.com/chenguuu/pysection',
    description="Current version provides ULS Checks (NTC-2018) for RC sections based on FEM database",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],
)