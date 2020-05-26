#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.1 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.2 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.3 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.4 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.5 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.6 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.7 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.8 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 0.9 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 1.0 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 1.25 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 1.5 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 1.75 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 2.0 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 4.0 $OUT/vary_rfrac
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 10000 6.0 $OUT/vary_rfrac
