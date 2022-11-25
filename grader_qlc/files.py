import os.path
import yaml

from .i18n import texts

OUTPUT_FILE = '/feedback/out'
CONFIG_FILE = '/exercise/config.yaml'
HTML_FILE = 'mg_qlc/aplus_template.html'
JS_FILE = 'mg_qlc/aplus_form.js'

the_dir = None

def read_config():
  with open(CONFIG_FILE) as f:
    return yaml.load(f)

def read_asset(name):
  if the_dir is None:
    the_dir = os.path.dirname(os.path.abspath(__file__))
  with open(os.path.join(the_dir, name), 'r') as f:
    return f.read()

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
            in_style = True
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

def rewrite_output(lang_code, previous_output):
  html = read_asset(HTML_FILE)
  js = read_asset(JS_FILE)
  with open(OUTPUT_FILE, 'w') as f:
    f.write(html.format({
      **texts.get(lang_code, texts['en']),
      **previous_output,
      'js_code': js,
    }))
