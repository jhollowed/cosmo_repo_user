#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac rfraclos nsrcs lenspix out_dir vis_flag
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 32 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 64 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 128 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 256 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 512 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 1024 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 2048 $OUT/vary_los 1
$PY make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 5000 4096 $OUT/vary_los 1

