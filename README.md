# grader_qlc

Augments existing
[mooc-grader](https://github.com/apluslms/mooc-grader)
programming assessments with
[Questions About Learners' Code (QLCs)](https://doi.org/10.1109/ICPC52881.2021.00054).
Such questions target concrete constructs and patterns in the program that
student previously created. Answering these questions has potentially
reflection and self-explanation benefits for learning.

#### Background

The mooc-grader and aplus ecosystem supports developing automatically assessed
(programming) exercises. The student submits their program code for grading and
the system executes tests against the program in a container environment.
Docker containers have been developed for testing programs in different 
programming languages and using different programming libraries.

#### Contribution

This package provides a tool `qlc_wrap` that can be added to existing
grading containers as described in **Usage**. The tool does not affect the
usual program grading behaviour. However, once the program is graded full
points, the tool analyses the program and generates questions. There are two
alternatives how the questions can be posed to the student.
*The first alternative is recommended over the second one.*

1. In addition to the normal feedback, the tool can store questionnaire data
   that is invisible for the student. The first alternative has no apparent
   effect on the programming exercise. The questionnaire is presented as an
   other exercise that has its own submissions and points. See
   `aplus_followups` directory for material to create the related exercise.

2. The normal feedback is altered so that the questionnaire appears as a new
   primary tab and the completed tests are pushed to a secondary tab. The
   questionnaire provides feedback but the answers are not graded for points.
   The student answer log can be stored by configuring an URL to a hidden
   exercise that collects statistics.

#### Dependencies

In addition to this package, question generation libraries are required for
the particular programming language that is used in the exercise.
* https://github.com/teemulehtinen/qlcpy (Python)
* https://github.com/teemulehtinen/qlcjs (JavaScript)

## Usage

#### Augmenting the grading container

`Dockerfile`
```Dockerfile
  # The grading image for the exercise which we extend
  FROM apluslms/grade-python:3.9-4.8-4.5

  RUN \
    pip_install \
      # The qlc_wrap tool
      https://github.com/teemulehtinen/grader_qlc/archive/v1.0.3.tar.gz \
      # For Python programs
      qlcpy==1.0.13 \
    # For JavaScript programs
    && npm install -g teemulehtinen/qlcjs
```

#### Configuring an exercise

`config.yaml`

```yaml
# ... other parts as before

container:
  # The augmented grading image containing grader_qlc
  image: registry.cs.aalto.fi/lehtint6/pyqlcs:1.3
  # As before
  mount: the_path/to_exercise
  # Prefix with the tool and rest as before
  cmd: qlc_wrap /exercise/run.sh

qlc:
  # Command to produce QLC json, see qlcpy --help
  cmd: ["qlcpy", "--json", "-un", "5", submitted.py"]

  # Optional files to display (default: all files submitted)
  files:
    - submitted.py
    - input.txt
  # Optional language (default: en)
  lang: en
  
  # To enable the 2. alternative, provide these POST directives
  # (tool replaces %n with the current path components)
  post_url: "%0/%1/module/chapter/hidden_exercise/"
  post_field: log_json
```

#### Usage

```
qlc_wrap [-LANGUAGE_CODE] grading command
```
If the first argument starts with `-`, it signals a language code. The 
configured `qlc.cmd` parts can include `$LANG` that is replaced with the
language code, `en` by default.

The suggested QLC generators support a plentiful amount of options that are
described in their documentation.
