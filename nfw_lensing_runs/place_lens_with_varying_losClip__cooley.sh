#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac rfraclos nsrcs lenspix out_dir vis_flag
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 0.2 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 0.4 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 0.6 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 0.8 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 1.0 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 1.2 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 1.4 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 1.6 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 1.8 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 2.0 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 3.0 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 4.0 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 5.0 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6.0 5000 1024 $OUT/vary_los 1

