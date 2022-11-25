import json
import subprocess
import sys

from .files import read_output, read_config, read_file, rewrite_output

def run_qlc(config):
  res = subprocess.run(config.get('cmd'), capture_output=True)
  return {
    'qlcs': json.loads(res.stdout),
    'files': list([name, read_file(name)] for name in config.get('files', [])),
    'post_url': config.get('post_url'),
    'post_field': config.get('post_field'),
  }

def run_wrapped(cmd_list):
  subprocess.run(cmd_list)
  output = read_output()
  if output['points'] >= output['max_points']:
    config = read_config()
    rewrite_output(config.get('lang'), output, run_qlc(config))

def wrap():
  if len(sys.argv) < 2:
    print('qlc_wrap must preceed grading command on the line')
    sys.exit(1)
  run_wrapped(sys.argv[1:])
