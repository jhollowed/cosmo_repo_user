#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests
$PY  make_and_raytrace_nfwBall.py 0.2 0.5 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 0.75 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.25 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.5 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.75 10000 6 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 2.0 10000 6 $OUT/vary_zs

