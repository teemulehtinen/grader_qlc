#!/usr/bin/python3
import os.path
import sys
import subprocess

# Execute normal grading in a separate process
subprocess.run(sys.argv[1:])

# Load external python package
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'mg_qlc'))
import mg_qlc

# Read the output from normal grading
output = mg_qlc.read_output()

# Augment QLCs if full grade
if output['points'] >= output['max_points']:
  
  # TODO qlc data
  
  mg_qlc.rewrite_output('fi', script_dir, output)
