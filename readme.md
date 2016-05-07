![Northwestern University](http://imgur.com/EfQ0qhf.png?1)

## Yelp Dataset Challenge

This repository contains python scripts for reading, manipulating, and preparing variables from the Yelp
Academic Dataset, used in an analytics competition at Northwestern University. Two python files,
*prep_data.py* and *simple_analytics.py*, are included as examples of how to extract variables from nested json
data using python's dictionary capability and how to perform ordinary least squares linear regression using python.

The final, prepped dataset is included in this repository. The original raw datasets are too large to include, but 
subsets of the original files and prepped dataset are included for testing. Be advised that due to the double for 
loops in the last portion of the *prep_data.py* script and lack of Cython/Numpy usage, prepping the dataset can 
take approximately six hours to convert to csv format.

### Dependencies

This was put together using Python 3.4.3. You'll need to install *pandas* in order to run the 
*simple_analytics.py* script. For processing the raw data using *prep_data.py*, no external python
libraries are needed other than the *tqdm* library for monitoring progress. 