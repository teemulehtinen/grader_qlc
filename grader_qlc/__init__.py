import subprocess
import sys

from .files import read_output, read_config, rewrite_output

def wrap():

  # Execute normal grading in a separate process
  if len(sys.argv) < 2:
    print('qlc_wrap must preceed grading command on a line')
    sys.exit(1)
  subprocess.run(sys.argv[1:])

  # Read the output from normal grading
  output = read_output()

  # Augment QLCs if full grade
  if output['points'] >= output['max_points']:
    
    config = read_config().get('qlc', {})
    # TODO qlc data

    rewrite_output(config.get('lang', 'en'), output)
