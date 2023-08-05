# klib

[![PyPI Version](https://img.shields.io/pypi/v/klib)](https://pypi.org/project/klib/)
[![Language](https://img.shields.io/github/languages/top/akanz1/klib)](https://pypi.org/project/klib/)
[![Downloads](https://img.shields.io/pypi/dw/klib)](https://pypi.org/project/klib/)
[![Last Commit](https://img.shields.io/github/last-commit/akanz1/klib)](https://github.com/akanz1/klib)
[![Build](https://scrutinizer-ci.com/g/akanz1/klib/badges/build.png?b=master)](https://github.com/akanz1/klib)
[![Activity](https://img.shields.io/github/commit-activity/m/akanz1/klib)](https://github.com/akanz1/klib)
[![Code Quality](https://scrutinizer-ci.com/g/akanz1/klib/badges/quality-score.png?b=master)](https://github.com/akanz1/klib)
[![License](https://img.shields.io/pypi/l/klib)](https://github.com/akanz1/klib/blob/master/LICENSE)

klib is a Python library for importing, cleaning, analyzing and preprocessing data. Future versions will include model creation and optimization to provide an end-to-end solution.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install klib.

```bash
pip install klib
pip install --upgrade klib
```

## Usage

```python
import klib

# klib.describe() # ...
klib.corr_plot() # returns a color-encoded heatmap, ideal for correlations
klib.missingval_plot() # returns a figure containing information about missing values

# Coming soon:
# klib.ingest() # ...
# klib.clean() # ...
# klib.preprocess() # ...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
