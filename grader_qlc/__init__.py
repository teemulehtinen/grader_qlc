import json
import subprocess
import sys

from .files import read_output, read_config, read_file, rewrite_output

def run_qlc(config):
  res = subprocess.run(config.get('cmd'), capture_output=True)
  data = {
    'qlcs': json.loads(res.stdout),
    'files': list([name, read_file(name)] for name in config.get('files', [])),
  }
  for key in ('post_url', 'post_field'):
    if key in config:
      data[key] = config[key]
  return data

def run_wrapped(cmd_list):
  subprocess.run(cmd_list)
  output = read_output()
  if output['points'] >= output['max_points']:
    config = read_config()
    data = run_qlc(config)
    rewrite_output(config.get('lang'), output, data, 'post_url' in data)

def wrap():
  if len(sys.argv) < 2:
    print('qlc_wrap must preceed grading command on the line')
    sys.exit(1)
  run_wrapped(sys.argv[1:])
