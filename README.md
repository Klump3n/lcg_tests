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

Run ```check_lcg.py```. For a bit more information about which tests are failing
and which are succeeding you can use ```check_lcg.py -l verbose```.

