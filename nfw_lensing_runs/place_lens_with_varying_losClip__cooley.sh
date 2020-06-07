#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac nsrcs out_dir vis_flag
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 0.2
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 0.4
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 0.6
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 0.7
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 0.8
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 1.0
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 1.2
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 1.4
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 1.6
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 1.8
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 2.0
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 3.0
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 4.0
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 5.0
$PY  make_and_raytrace_nfwBall.py 0.2  1.0 20000 6 2000 $OUT/vary_los 1 6.0

