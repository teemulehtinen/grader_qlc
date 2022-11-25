CONFIG_CONTENT = """
view_type: access.types.stdasync.acceptFiles
files:
  - field: file1
    name: submitted.py

container:
  image: teemule/grade-python-qlc:latest
  mount: my_exercise_path
  cmd: qlc_wrap my_exercise_run

qlc:
  cmd: ["cat", "sample.json"]
  post_url: "%0/%1/foo/"
  post_field: log_json
  lang: en
"""

OUT_CONTENT = """
<style>
h1 { font-size: 100; }
</style>
<p>
My test results here!
</p>

TotalPoints: 10
MaxPoints: 10
"""

SUBMITTED = "submitted-content"
QLC_JSON = '["aa", "be", "ce"]'
