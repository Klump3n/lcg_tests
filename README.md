# A testing suite for linear congruential generators

### What this is

This is part of a seminar I'm taking at university. The goal is to find
combinations of parameters that fulfill statistical tests (monobit, poker, etc)
but fail the spectral test. Apparently the spectral test revealed that people
used crappy "random numbers" for a very long time because they were not aware
that they are not at all random, but fall into certain hyperplanes.

For the theory part of linear congruential generators (LCGs) please refer to [the corresponding seminar homepage](https://zufallsmaschiness19.github.io/LCG/lcg.html).

### What this is NOT

This testing suite does not do anything as fancy as the DIEHARD suite (or
similar suites for that matter). Do not expect new tests.

## Contents

This package contains two scripts.
 * ```lcong.py``` is a script that can create pseudo random numbers with an LCG with varying paramters. It then performs statistical tests and the spectral test on these numbers. It can also read in binary numbers from a text file and perform the statistical tests on them. The results of the LCG analysis are stored in pickled files.
 * ```plot_results.py``` is a script that reads the pickled results files and can display the results.

## Usage

### Single sets of parameters

Testing a specific combination of parameters (in this case this is the set of parameters for the C++ LCG) is done like this: ```./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31 - 1"```. The results are then logged to the screen.
```
[19.06.2019 19:52:09,753; INFO] Starting LCG testing
[19.06.2019 19:52:09,753; INFO] Skipping parameters where the results are already calculated
[19.06.2019 19:52:09,753; INFO] To disable skipping consider setting the '-f' flag
[19.06.2019 19:52:09,753; INFO] Created 1 parameters
[19.06.2019 19:52:09,753; INFO] At one second per check this will take about 1 seconds (or 0.02 minutes; or 0.00 hours)
[19.06.2019 19:52:10,787; INFO] [1 of 1]: (5/5 passes) statistical tests PASSED || spectral test PASSED for parameters {'x0': 1, 'a': 1103515245, 'c': 12345, 'm': 2147483647}
[19.06.2019 19:52:10,787; INFO] Results written to file [...]/lcg_tests/results/results_x0_1_a_1103515245_1103515245_c_12345_12345_m_2147483647_2147483647.pickle
```

Or more verbose:
```./lcong.py -x 1 -a 1103515245 -c 12345 -m "2**31 - 1" -l verbose```

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

Test results are stored in an output file in the ```results``` directory.

### Parameter sweeps

A parameter sweep is also possible. For this we simply supply the command line arguments ```-a```, ```-c``` and/or ```-m``` with two values: ```./lcong.py -x 1 -a "7**7 - 10" "7**7 + 10" -c 0 -m "2**31 - 10" "2**31 + 10"```

```
[19.06.2019 20:03:10,570; INFO] Starting LCG testing
[19.06.2019 20:03:10,570; INFO] Skipping parameters where the results are already calculated
[19.06.2019 20:03:10,570; INFO] To disable skipping consider setting the '-f' flag
[19.06.2019 20:03:10,571; INFO] Created 441 parameters
[19.06.2019 20:03:10,571; INFO] At one second per check this will take about 441 seconds (or 7.35 minutes; or 0.12 hours)
[19.06.2019 20:03:11,603; INFO] [1 of 441]: (5/5 passes) statistical tests PASSED || spectral test FAILED for parameters {'x0': 1, 'a': 823533, 'c': 0, 'm': 2147483638}
[19.06.2019 20:03:12,653; INFO] [2 of 441]: (4/5 passes) statistical tests FAILED || spectral test FAILED for parameters {'x0': 1, 'a': 823534, 'c': 0, 'm': 2147483638}
[19.06.2019 20:03:13,699; INFO] [3 of 441]: (4/5 passes) statistical tests FAILED || spectral test FAILED for parameters {'x0': 1, 'a': 823535, 'c': 0, 'm': 2147483638}
[19.06.2019 20:03:14,749; INFO] [4 of 441]: (4/5 passes) statistical tests FAILED || spectral test FAILED for parameters {'x0': 1, 'a': 823536, 'c': 0, 'm': 2147483638}
[19.06.2019 20:03:15,804; INFO] [5 of 441]: (3/5 passes) statistical tests FAILED || spectral test FAILED for parameters {'x0': 1, 'a': 823537, 'c': 0, 'm': 2147483638}
[...]
```

In case the calculation gets interrupted and picked up again at a later time, already calculated values will be read from the pickled output file and thus skipped. This can save a lot of time. In order to force recalculation for every timestep, we can supply the ```-f``` flag.

### Checking your own random binary sequences

To perform the tests on a sequence of random bits that you have you can run
```lcong.py -i RANDOM_DATA_FILE```, where RANDOM_DATA_FILE contains
your random bits. Some random data is provided in the directory ```random_sequences/```.

If you want to supply your own random numbers you have to present them in form of a binary sequence string (e.g. "001010101000") and save that to a text file.

Run ```lcong.py -h``` for a full list of options.

### Analyzing the results

The stored results can be viewed with the script ```plot_results.py```. Use the ```-i``` argument followed by the results*.pickle file.After some checks you are presented with three lists: ```./plot_results.py -i [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658.pickle```

```
[19.06.2019 20:15:02,063; INFO] Using [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658.pickle
[19.06.2019 20:15:02,067; INFO]  a is in [823533, 823553]
[19.06.2019 20:15:02,067; INFO]  c is in [0, 0]
[19.06.2019 20:15:02,067; INFO]  m is in [2147483638, 2147483658]
[19.06.2019 20:15:02,067; INFO] Pick ONE value from the ranges to generate a plot
```

We have done a scan with the fixed value ```c = 0```, while a and c vary. So now set the ```-c 0``` flag.
```./plot_results.py -i [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658.pickle -c 0```

The figures that now pop up can be stored next to the pickled results files in form of .png images. To do this append the ```-o``` flag: ```./plot_results.py -i [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658.pickle -c 0 -o```

```
[19.06.2019 20:18:38,483; INFO] Using [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658.pickle
[19.06.2019 20:18:38,579; INFO] Generating [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658_statistical_c_is_0.png
[19.06.2019 20:18:38,835; INFO] Generating [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658_spectral_c_is_0.png
[19.06.2019 20:18:38,974; INFO] Generating [...]/lcg_tests/results/results_x0_1_a_823533_823553_c_0_0_m_2147483638_2147483658_spectral_if_statistical_c_is_0.png
```

