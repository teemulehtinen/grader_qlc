import json
import subprocess
import sys

from .files import read_output, read_config, read_file, rewrite_output

def run_qlc(config, qlc_lang='en'):
  cmd = list(p if p != '$LANG' else qlc_lang for p in config.get('cmd'))
  res = subprocess.run(cmd, capture_output=True)
  data = {
    'qlcs': json.loads(res.stdout),
    'files': list([name, read_file(name)] for name in config.get('files', [])),
  }
  for key in ('post_url', 'post_field'):
    if key in config:
      data[key] = config[key]
  return data

def run_wrapped(cmd_list, qlc_lang='en'):
  subprocess.run(cmd_list)
  output = read_output()
  if output['points'] >= output['max_points']:
    config = read_config()
    data = run_qlc(config, qlc_lang)
    rewrite_output(config.get('lang'), output, data, 'post_url' in data)

def wrap():
  if len(sys.argv) < 2:
    print('qlc_wrap must preceed grading command on the line')
    sys.exit(1)
  if sys.argv[1].startswith('-'):
    run_wrapped(sys.argv[2:], sys.argv[1][1:])
  else:
    run_wrapped(sys.argv[1:])
