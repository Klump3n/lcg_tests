# A testing suite for linear congruential generators

## What this is

This is part of a seminar I'm taking at university. The goal is to find
combinations of parameters that fulfill statistical tests (monobit, poker, etc)
but fail the spectral test. Apparently the spectral test revealed that people
used crappy "random numbers" for a very long time because they were not aware
that they are not at all random, but fall into certain hyperplanes.

## What this is NOT

This testing suite does not do anything as fancy as the DIEHARD suite (or
similar suites for that matter). Do not expect new tests.

# Usage

Run ```lcong.py -h``` for a full list of options. For a bit more information about which tests are failing
and which are succeeding you can use the ```-l verbose``` flag (or even ```-l debug```).

To perform the tests on a sequence of random bits that you have you can run
```lcong.py -f RANDOM_DATA_FILE [-l verbose]```, where RANDOM_DATA_FILE contains
your random bits. Some random data is provided in ```random_sequences/```.

* rand* are from random.org
* benson_rand is from a quantum random number generator

If you want to supply your own random numbers you have to present them in form of a binary sequence string (e.g. "001010101000") and save that to a text file.

The arguments ```-a```, ```-c``` and ```-m``` can be used with one OR two arguments. If one argument is supplied, a random number sequence with that exact argument is generated. If two arguments are used, a random number sequence will be generated for every parameter between the two provided argument values.

The results will be save to an output file (pickled). If you want to force recalculation of existing values, use the ```-f``` flag.

The stored results can be viewed with the script ```plot_results.py```. Use the ```-i``` argument followed by the results*.pickle file.After some checks you are presented with three lists.

```
[19.06.2019 19:25:29,152; INFO] Using results/results_x0_1_a_1_10_c_0_10_m_251232131_251232131.pickle
[19.06.2019 19:25:29,154; INFO]  a is in [1, 10]
[19.06.2019 19:25:29,154; INFO]  c is in [0, 10]
[19.06.2019 19:25:29,154; INFO]  m is in [251232131, 251232131]
[19.06.2019 19:25:29,154; INFO] Pick ONE value from the ranges to generate a plot

```

We have done a scan with the fixed value ```m = 251232131```, while a and c vary. So now set the ```-m 251232131``` flag and look at the results. They can be saved into .png files with the ```-o``` flag.
