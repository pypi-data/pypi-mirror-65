import setuptools
from pathlib import Path

setuptools.setup(
    name = 'joetags',
    version = '0.2.1',
    description=('tag and organize your projects'),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    maintainer="realsirjoe",
    author="realsirjoe",
    entry_points = {
        'console_scripts': [
            'joetags = joetags.__main__:main',
            'jt = joetags.__main__:main'
        ]
    })
