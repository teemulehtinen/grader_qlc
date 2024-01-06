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

QLC_DATA = {
  "qlcs": ["qlc1", "qlc2"],
  "files": [["file1", "content1"], ["file2", "content2"]],
}
QLC_POST_DATA = {
  **QLC_DATA,
  "post_url": "/form/store",
  "post_field": "qlc_data",
}

SUBMITTED = "submitted-content"
QLC_JSON = ["aa", "be", "ce"]
