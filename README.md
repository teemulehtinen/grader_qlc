# grader_qlc

Augments existing
[mooc-grader](https://github.com/apluslms/mooc-grader)
programming assessments with
[Questions About Learners' Code (QLCs)](https://doi.org/10.1109/ICPC52881.2021.00054).
Such questions target concrete constructs and patterns in the program that
student previously created. Answering these questions has potentially
reflection and self-explanation benefits for learning.

In more words, the mooc-grader platform supports developing automatically
assessed (programming) exercises. The student submits their program code for
grading and the platform executes tests against the program in a container
environment. Docker containers have been developed for different programming
languages and libraries that the students may use.

This package provides a tool that can be added to existing containers for
augmenting the program test outputs with questionnaire about the structure and
functionality of the tested program. The tool checks the previous output and
augments it with hidden questionnaire data.

The hidden questionnaire data can be read in another exercise to create and
grade an answer form. Alternatively, this tool can create an answer form
inside the feedback and record the answer log to another hidden exercise.
The second alternative is enabled by providing a post_url in the config.

In addition to this package, question generation libraries are required for
the particular programming language that is used in the exercise.
* https://github.com/teemulehtinen/qlcpy (Python)
* https://github.com/teemulehtinen/qlcjs (JavaScript)

## Deriving a container

`Dockerfile`
```Dockerfile
  # The image to be extended
  FROM ...

  RUN pip_install \
    https://github.com/teemulehtinen/grader_qlc/archive/v1.0.1.tar.gz
```

The generation requirements for the language are also required, e.g.
* `RUN pip_install qlcpy`
* `RUN npm install -g teemulehtinen/qlcjs`

## Augmenting an exercise

`config.yaml`

```yaml
container:
  # The new image containing grader_qlc
  image: ...
  # As before
  mount: the_path/to_exercise
  # After the prefix as before
  cmd: qlc_wrap /exercise/run.sh

qlc:
  # Command to produce QLC json
  cmd: ["qlcpy", "--json", "submitted.py"]
  # Optional POST URL (%n is replaced by the current path components)
  post_url: "%0/%1/module/chapter/hidden_exercise/"
  # Optional POST field name (used to send answer log as json)
  post_field: log_json
  # Optional files to display (default: all files submitted)
  files:
    - submitted.py
    - input.txt
  # Optional language (default: en)
  lang: en
```