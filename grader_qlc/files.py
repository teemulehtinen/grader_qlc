import json
import os.path
import yaml

from .i18n import texts

OUTPUT_FILE = '/feedback/out'
CONFIG_FILE = '/exercise/config.yaml'
HTML_FILE = 'aplus_template.html'
JS_FILES = ['aplus_form.js', 'simple-quiz-form.js']

def read_config():
  with open(CONFIG_FILE) as f:
    full_config = yaml.safe_load(f)
  config = full_config.get('qlc', {})
  if not 'files' in config:
    config['files'] = list(f['name'] for f in full_config.get('files', []))
  return config

def read_file(path):
  if not os.path.exists(path):
    return ''
  with open(path, 'r') as f:
    return f.read()

def read_asset_file(name):
  return read_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), name))

def read_output():
  style_lines = []
  test_lines = []
  point_lines = []
  with open(OUTPUT_FILE) as f:
    in_style = False
    for line in f:
      if line.startswith('TotalPoints: '):
        points = int(line[13:])
        point_lines.append(line)
      elif line.startswith('MaxPoints: '):
        max_points = int(line[11:])
        point_lines.append(line)
      else:
        if not in_style:
          if '<style>' in line:
            in_style = not '</style>' in line
            style_lines.append(line)
          else:
            test_lines.append(line)
        else:
          if '</style>' in line:
            in_style = False
          style_lines.append(line)
  return {
    'style_html': ''.join(style_lines),
    'test_html': ''.join(test_lines),
    'points_footer': ''.join(point_lines),
    'points': points,
    'max_points': max_points,
  }

def rewrite_output(lang_code, previous_output, qlc_data):
  html = read_asset_file(HTML_FILE)
  js = '\n\n'.join(read_asset_file(name) for name in JS_FILES)
  with open(OUTPUT_FILE, 'w') as f:
    f.write(html.format(**{
      **texts.get(lang_code, texts['en']),
      **previous_output,
      'js_code': js,
      'qlc_json': json.dumps(qlc_data),
    }))
