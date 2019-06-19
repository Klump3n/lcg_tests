# A testing suite for linear congruential generators

### What this is

This is part of a seminar I'm taking at university. The goal is to find
combinations of parameters that fulfill statistical tests (monobit, poker, etc)
but fail the spectral test. Apparently the spectral test revealed that people
used crappy "random numbers" for a very long time because they were not aware
that they are not at all random, but fall into certain hyperplanes.

### What this is NOT

This testing suite does not do anything as fancy as the DIEHARD suite (or
similar suites for that matter). Do not expect new tests.

## Contents

This package contains two scripts.
 * ```lcong.py``` is a script that can create pseudo random numbers with a linear congruential generator (LCG) with varying paramters. It then performs statistical tests and the spectral test on these numbers. It can also read in binary numbers from a text file and perform the statistical tests on them. The results of the LCG analysis are stored in pickled files.
 * ```plot_results.py``` is a script that reads the pickled results files and can display the results.

## Usage

Testing a specific combination of parameters is done like this: ```./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31 - 1"```. The results are then logged to the screen
```
[19.06.2019 19:52:09,753; INFO] Starting LCG testing
[19.06.2019 19:52:09,753; INFO] Skipping parameters where the results are already calculated
[19.06.2019 19:52:09,753; INFO] To disable skipping consider setting the '-f' flag
[19.06.2019 19:52:09,753; INFO] Created 1 parameters
[19.06.2019 19:52:09,753; INFO] At one second per check this will take about 1 seconds (or 0.02 minutes; or 0.00 hours)
[19.06.2019 19:52:10,787; INFO] [1 of 1]: (5/5 passes) statistical tests PASSED || spectral test PASSED for parameters {'x0': 1, 'a': 1103515245, 'c': 12345, 'm': 2147483647}
[19.06.2019 19:52:10,787; INFO] Results written to file [...]/lcg_tests/results/results_x0_1_a_1103515245_1103515245_c_12345_12345_m_2147483647_2147483647.pickle
```
or more verbose ```./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31 - 1" -l verbose```.

```
[19.06.2019 19:56:14,913; VERBOSE] starting logging
[19.06.2019 19:56:14,913; VERBOSE] logging level is set to verbose

[19.06.2019 19:56:14,913; INFO] Starting LCG testing
[19.06.2019 19:56:14,913; VERBOSE] Using 4 processes in parallel (in (long) runs test)
[19.06.2019 19:56:14,913; INFO] Skipping parameters where the results are already calculated
[19.06.2019 19:56:14,913; INFO] To disable skipping consider setting the '-f' flag
[19.06.2019 19:56:14,914; VERBOSE] Using results file [...]/lcg_tests/results/results_x0_1_a_1103515245_1103515245_c_12345_12345_m_2147483647_2147483647.pickle
[19.06.2019 19:56:14,914; INFO] Created 1 parameters
[19.06.2019 19:56:14,914; INFO] At one second per check this will take about 1 seconds (or 0.02 minutes; or 0.00 hours)
[19.06.2019 19:56:14,914; VERBOSE] Generating pseudorandom numbers for parameters x0 = 1, a = 1103515245, c = 12345, m = 2147483647
[19.06.2019 19:56:14,922; VERBOSE] Padding numbers to 31 digits
[19.06.2019 19:56:14,933; VERBOSE] Performing MONOBIT test
[19.06.2019 19:56:14,937; VERBOSE] Monobit test passed, ratio is 0.4962
[19.06.2019 19:56:14,937; VERBOSE] Performing POKER test
[19.06.2019 19:56:14,939; VERBOSE] Poker test passed, result is 24.0064
[19.06.2019 19:56:14,939; VERBOSE] Performing RUNS test
[19.06.2019 19:56:14,950; VERBOSE] Runs test: 2432 0 runs and 2429 1 runs of length 1
[19.06.2019 19:56:14,961; VERBOSE] Runs test: 1243 0 runs and 1275 1 runs of length 2
[19.06.2019 19:56:14,972; VERBOSE] Runs test: 589 0 runs and 622 1 runs of length 3
[19.06.2019 19:56:14,984; VERBOSE] Runs test: 351 0 runs and 309 1 runs of length 4
[19.06.2019 19:56:14,996; VERBOSE] Runs test: 170 0 runs and 170 1 runs of length 5
[19.06.2019 19:56:15,513; VERBOSE] Runs test: 162 0 runs and 142 1 runs of length 6+
[19.06.2019 19:56:15,514; VERBOSE] Runs test passed, all within tolerance
[19.06.2019 19:56:15,514; VERBOSE] Performing LONG RUNS test
[19.06.2019 19:56:15,826; VERBOSE] Long runs test passed, no long runs
[19.06.2019 19:56:15,826; VERBOSE] Performing AUTOCORRELATION test
[19.06.2019 19:56:15,947; VERBOSE] Autocorrelation test passed, no correlations found
[19.06.2019 19:56:15,948; VERBOSE] Performing SPECTRAL test
[19.06.2019 19:56:15,948; VERBOSE] Test for 2 dimensions passed when v2 = 45096.01 > 32768, so it passed
[19.06.2019 19:56:15,950; VERBOSE] Test for 3 dimensions passed when v3 = 1279.36 > 1024.00, so it passed
[19.06.2019 19:56:15,951; VERBOSE] Test for 4 dimensions passed when v4 = 195.21 > 181.02, so it passed
[19.06.2019 19:56:15,953; VERBOSE] Test for 5 dimensions passed when v5 = 67.79 > 64.00, so it passed
[19.06.2019 19:56:15,954; INFO] [1 of 1]: (5/5 passes) statistical tests PASSED || spectral test PASSED for parameters {'x0': 1, 'a': 1103515245, 'c': 12345, 'm': 2147483647}
[19.06.2019 19:56:15,954; INFO] Results written to file [...]/lcg_tests/results/results_x0_1_a_1103515245_1103515245_c_12345_12345_m_2147483647_2147483647.pickle
```



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
