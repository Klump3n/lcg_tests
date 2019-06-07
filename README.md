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

## Usage

Run ```lcong.py -h``` for a full list of options. For a bit more information about which tests are failing
and which are succeeding you can use the ```-l verbose``` flag (or even ```-l debug```).

To perform the tests on a sequence of random bits that you have you can run
```lcong.py -f RANDOM_DATA_FILE [-l verbose]```, where RANDOM_DATA_FILE contains
your random bits. Some random data is provided in ```random_sequences/```.

* rand* are from random.org
* benson_rand is from a quantum random number generator

If you want to supply your own random numbers you have to present them in form of a binary sequence string (e.g. "001010101000") and save that to a text file.

The arguments ```-a```, ```-c``` and ```-m``` can be used with one OR two arguments. If one argument is supplied, a random number sequence with that exact argument is generated. If two arguments are used, a random number sequence will be generated for every parameter between the two provided argument values.
