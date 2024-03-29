#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/convergence_tests_fixedprof

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac rfraclos nsrcs lenspix out_dir vis_flag
$PY  make_and_raytrace_nfwBall.py 0.05 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
#$PY make_and_raytrace_nfwBall.py 0.1 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
$PY make_and_raytrace_nfwBall.py 0.2 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
#$PY make_and_raytrace_nfwBall.py 0.3 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
$PY make_and_raytrace_nfwBall.py 0.4 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
#$PY make_and_raytrace_nfwBall.py 0.5 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
$PY make_and_raytrace_nfwBall.py 0.6 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
#$PY make_and_raytrace_nfwBall.py 0.7 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
$PY make_and_raytrace_nfwBall.py 0.8 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe
#$PY make_and_raytrace_nfwBall.py 0.9 1.0 10000 6 6 200 1024 $OUT/vary_zl 1 dtfe

