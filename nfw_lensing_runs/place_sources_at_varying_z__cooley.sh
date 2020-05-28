#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests
$PY  make_and_raytrace_nfwBall.py 0.2 0.5 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 0.75 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.25 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.5 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 1.75 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 2.0 20000 6 10000 $OUT/vary_zs
$PY  make_and_raytrace_nfwBall.py 0.2 2.25 20000 6 10000 $OUT/vary_zs

