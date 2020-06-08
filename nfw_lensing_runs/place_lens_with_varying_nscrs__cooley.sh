#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac rfraclos nsrcs lenspix out_dir vis_flag
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 100 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 500 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 1000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 1500 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 2000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 2500 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 3000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 3500 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 4000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 4500 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 10000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 20000 1024 $OUT/vary_los 1

