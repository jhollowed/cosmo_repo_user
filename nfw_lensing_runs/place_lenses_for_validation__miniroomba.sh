#!/bin/bash

PY=/miniconda3/bin/python
OUT=/Users/joe/repos/repo_user/nfw_validation/validation_halos

# Calling format is make_and_raytrace_NFWBall.py zl zs N rfrac rfraclos nsrcs lenspix out_dir vis_flag de_type, seed, skip_raytace_flag
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 101 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 202 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 303 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 404 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 505 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 606 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 707 0
$PY  make_and_raytrace_nfwBall.py 0.2 1.0 20000 6 6 200 1024 $OUT 1 dtfe 808 0

