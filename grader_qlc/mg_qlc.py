import os

FEEDBACK_FILE = '/feedback/out'
HTML_FILE = 'mg_qlc/aplus_template.html'
JS_FILE = 'mg_qlc/aplus_form.js'

i18n = {
  'en': {
    'qlc_tab': 'Follow-up questions',
    'test_tab': 'Test results',
    'title': 'That\'s correct!',
    'intro': (
      'Your program passed all the tests which can be viewed on the other tab.'
      'Now, check the level of your understanding by answering the following questions:'
    )
  },
  'fi': {
    'qlc_tab': 'Jatkokysymykset',
    'test_tab': 'Testitulokset',
    'title': 'Oikein meni!',
    'intro': (
      'Ohjelmasi läpäisi kaikki testit, jotka ovat nähtävissä toisella välilehdellä.'
      'Nyt voit tarkistaa osaamistasi vastaamalla seuraaviin kysymyksiin:'
    )
  }
}

def read_output():
  style_lines = []
  test_lines = []
  point_lines = []
  with open(FEEDBACK_FILE) as f:
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

def rewrite_output(lang_code, script_path, previous_output):
  with open(os.path.join(script_path, HTML_FILE), 'r') as f:
    html = f.read()
  with open(os.path.join(script_path, JS_FILE), 'r') as f:
    js = f.read()
  with open(FEEDBACK_FILE, 'w') as f:
    f.write(html.format({
      **i18n.get(lang_code, i18n['en']),
      **previous_output,
      'js_code': js,
    }))
