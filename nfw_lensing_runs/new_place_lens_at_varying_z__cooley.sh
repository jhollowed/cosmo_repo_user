#!/bin/bash

PY=/home/hollowed/anaconda3/bin/python
$PY  make_and_raytrace_nfwBall.py 0.01 1.0 10000 6 ./output2/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.1  1.0 10000 6 ./output2/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.3  1.0 10000 6 ./output2/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.5  1.0 10000 6 ./output2/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.7  1.0 10000 6 ./output2/vary_zl
$PY  make_and_raytrace_nfwBall.py 0.9  1.0 10000 6 ./output2/vary_zl

