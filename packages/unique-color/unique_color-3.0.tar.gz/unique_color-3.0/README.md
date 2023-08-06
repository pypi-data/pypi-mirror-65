[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3746984.svg)](https://doi.org/10.5281/zenodo.3746984)


# Summary

Provide 33 unique colors in hex or rgb format.

![example](33_unique_colors.png)

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


