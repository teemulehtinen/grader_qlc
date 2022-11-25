import os
import unittest

from grader_qlc import files, run_wrapped
from .sample_content import CONFIG_CONTENT, OUT_CONTENT, SUBMITTED, QLC_JSON

class TestFiles(unittest.TestCase):

  def setFile(self, name, content):
    with open(name, 'w') as f:
      f.write(content)

  def setUp(self):
    files.OUTPUT_FILE = 'out'
    files.CONFIG_FILE = 'config.yaml'
    self.setFile(files.OUTPUT_FILE, OUT_CONTENT)
    self.setFile(files.CONFIG_FILE, CONFIG_CONTENT)
    self.setFile('submitted.py', SUBMITTED)
    self.setFile('sample.json', QLC_JSON)
  
  def tearDown(self):
    os.remove(files.OUTPUT_FILE)
    os.remove(files.CONFIG_FILE)
    os.remove('submitted.py')
    os.remove('sample.json')

  def test_run(self):
    run_wrapped(['sleep', '0'])
    with open(files.OUTPUT_FILE, 'r') as f:
      out = f.read()
    self.assertTrue('qlcaug({"qlcs": ["aa", "be", "ce"], "files": [["submitted.py", "submitted-content"]], "post_url": "%0/%1/foo/", "post_field": "log_json"});' in out)
    self.assertTrue('My test results here!' in out)
