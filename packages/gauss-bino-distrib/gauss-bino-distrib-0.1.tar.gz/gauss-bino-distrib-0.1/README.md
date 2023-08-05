# Distribution
Generic distribution class for calculating and visualizing a probability distribution.
Parent class for Gaussian and Binomial.

### Available Methods

- `read_data_file()`
    Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute. After reading in the file, the mean and standard deviation are calculated.


## Gaussian

Gaussian distribution class for calculating and visualizing a Gaussian distribution.

### Available Methods

- `calculate_mean()` 
    Function to calculate the mean of the data set.
- `calculate_stddev()` 
    Function to calculate the standard deviation of the data set.
- `read_data_file()`
    Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute. After reading in the file, the mean and standard deviation are calculated.
- `plot_histogram()`
    Function to output a histogram of the instance variable data.
- `pdf()`
    Probability density function calculator for the gaussian distribution.
- `plot_histogram_pdf()`
    Function to plot the normalized histogram of the data and a plot of the probability density function along the same range.

### Available Operations

- Addition of Two Gaussian Deviation

### Representation Format

`"mean {}, standard deviation {}".format(self.mean, self.stdev)

## Binomial
Binomoal distribution class for calculating and visualizing a Binomial distribution.

### Available Methods

- `calculate_mean()` 
    Function to calculate the mean of the data set.
- `calculate_stddev()` 
    Function to calculate the standard deviation of the data set.
- `replace_stats_with_data()`
    Function to calculate p and n from the data set
- `plot_bar()`
    Function to output a histogram of the instance variable data using matplotlib pyplot library.
- `pdf()`
    Probability density function calculator for the distribution.
- `plot_bar_pdf()`
    Function to plot the pdf of the binomial distribution

### Available Operations

- Addition of Two Binomial Distributions with same p.

### Representation Format

`"mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)

