# ARGALI

## Descriptive Statistics
Descriptive statistics provide insight around dispersion and central tendency.

### Univariate

The univatiate descriptive statistics class provides easy access to a wide range of variables that are easily
accessible via a set of intuitively named functions.

The summary function provides key details relating to the variable and provides a four plots that exposure the structure
and distribution of the data.

Usage:

    from argali import descriptive_statistics

    x = [1, 2, 3, 4, 3, 4, 5, 6, 7, 6, 7, 8, 7, 8, 8, 6, 5, 44, 3, 4, 5, 6, 7, 8, 9, 33, 22, 11, -1]

    x_summary = descriptive_statistics.Univariate(data=x)

    x_summary.descriptive_summary()
