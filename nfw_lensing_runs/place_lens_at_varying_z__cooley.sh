#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests
$PY  make_and_raytrace_nfwBall.py 0.01 1.0 10000 6 $OUT/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.1  1.0 10000 6 $OUT/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.3  1.0 10000 6 $OUT/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.5  1.0 10000 6 $OUT/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.7  1.0 10000 6 $OUT/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.9  1.0 10000 6 $OUT/vary_zl

