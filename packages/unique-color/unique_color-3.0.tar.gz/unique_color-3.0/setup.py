from setuptools import setup, find_packages

long_description="""

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3746984.svg)](https://doi.org/10.5281/zenodo.3746984)


# Summary

Provide 33 unique colors in hex or rgb format.

![example](https://raw.githubusercontent.com/YichaoOU/unique_color/master/33_unique_colors.png)

# Installation

`pip install unique-color`

OR


```

git clone https://github.com/YichaoOU/unique_color

cd unique_color

python setup.py install

```

# Usage

The following command return a list of 33 colors.

```

from unique_color import unique_color as uc

my_colors = uc.unique_color()

my_colors = uc.unique_color_hex()

my_colors = uc.unique_color_rgb()


```



"""

setup(
    name='unique_color',
    version='3.0',
    author='Yichao Li',
    author_email='yl079811@ohio.edu',
    url='https://github.com/YichaoOU/unique_color',
	packages=['unique_color'],
    license='LICENSE',
    description='Provide 33 unique colors in hex or rgb format',
	long_description=long_description,
	long_description_content_type='text/markdown'	,
)


# python setup.py sdist
# python setup.py bdist_wheel --universal
# test the distributions
# twine upload dist/*