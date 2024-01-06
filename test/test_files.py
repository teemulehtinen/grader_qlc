import os
import unittest
import json

from grader_qlc import files
from .sample_content import (
  CONFIG_CONTENT, OUT_CONTENT, QLC_DATA, QLC_POST_DATA
)
class TestFiles(unittest.TestCase):

  def setFile(self, name, content):
    with open(name, 'w') as f:
      f.write(content)

  def setUp(self):
    files.OUTPUT_FILE = 'out'
    files.CONFIG_FILE = 'config.yaml'
    self.setFile(files.OUTPUT_FILE, OUT_CONTENT)
    self.setFile(files.CONFIG_FILE, CONFIG_CONTENT)
  
  def tearDown(self):
    os.remove(files.OUTPUT_FILE)
    os.remove(files.CONFIG_FILE)

  def test_config(self):
    config = files.read_config()
    self.assertEqual(config['cmd'], ['cat', 'sample.json'])
    self.assertEqual(config['post_url'], '%0/%1/foo/')
    self.assertEqual(config['post_field'], 'log_json')
    self.assertEqual(config['lang'], 'en')
    self.assertEqual(config['files'], ['submitted.py'])

  def test_read(self):
    out = files.read_output()
    self.assertNotEqual(out['style_html'].strip(), '')
    self.assertNotEqual(out['test_html'].strip(), '')
    self.assertNotEqual(out['points_footer'].strip(), '')
    self.assertEqual(out['points'], 10)
    self.assertEqual(out['max_points'], 10)

  def test_write(self):
    initial_output = files.read_output()
    files.rewrite_output('en', initial_output, QLC_DATA)
    out = files.read_output()
    self.assertTrue(json.dumps(QLC_DATA) in out['test_html'])
    self.assertEqual(out['points'], 10)
    self.assertEqual(out['max_points'], 10)
    files.rewrite_output('en', initial_output, QLC_POST_DATA, True)
    out = files.read_output()
    self.assertTrue(json.dumps(QLC_POST_DATA) in out['test_html']) 
    self.assertTrue('<script>' in out['test_html'])
    self.assertEqual(out['points'], 10)
    self.assertEqual(out['max_points'], 10)
