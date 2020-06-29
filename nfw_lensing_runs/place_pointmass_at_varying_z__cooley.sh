#!/bin/bash

#PY=/miniconda3/bin/python
#OUT=/Users/joe/repos/repo_user/nfw_lensing_runs/output_pointmass
PY=/home/hollowed/anaconda3/bin/python
OUT=/projects/DarkUniverse_esp/jphollowed/profile_fitting_tests/pointmass_tests

# Calling format is make_and_raytrace_NFWBall.py zl zs fov_size nsrcs lenspix out_dir vis_flag
$PY make_and_raytrace_pointMass.py 0.35 0.8 1 0.05 500 1024 $OUT/vary_zl 1 sph grid

#$PY make_and_raytrace_pointMass.py 0.05 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.1 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.2 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.3 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.4 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.5 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.6 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.7 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.8 1.0 1 500 1024 $OUT/vary_zl 1
#$PY make_and_raytrace_pointMass.py 0.9 1.0 1 500 1024 $OUT/vary_zl 1

