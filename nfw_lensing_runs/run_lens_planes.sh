#!/bin/bash

#PY=/miniconda3/bin/python
PY=/home/hollowed/anaconda3/bin/python
$PY ./make_simple_halo.py 0.1
$PY ./make_simple_halo.py 0.2
$PY ./make_simple_halo.py 0.3
$PY ./make_simple_halo.py 0.4
$PY ./make_simple_halo.py 0.5
$PY ./make_simple_halo.py 0.6

$PY ./raytrace_simple_halo.py 0.1
$PY ./raytrace_simple_halo.py 0.2
$PY ./raytrace_simple_halo.py 0.3
$PY ./raytrace_simple_halo.py 0.4
$PY ./raytrace_simple_halo.py 0.5
$PY ./raytrace_simple_halo.py 0.6
