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
augmenting the program test outputs with QLC questions. The tool checks the
previous output and can augment it with a question form that can store the
student's answers via JavaScript POST. In addition to this package, question
generation libraries are required for the particular programming language that
is used in the exercise.

* https://github.com/teemulehtinen/qlcpy (Python)
* https://github.com/teemulehtinen/qlcjs (JavaScript)

## Deriving a container

`Dockerfile`

    # The image to be extended
    FROM ...

    RUN pip_install \
      https://github.com/teemulehtinen/grader_qlc/archive/v1.0.0.tar.gz

The generation requirements for the language are also required, e.g.

* `RUN pip_install qlcpy`
* `RUN npm install -g teemulehtinen/qlcjs`

## Augmenting an exercise

`config.yaml`

    container:
      # The new image containing grader_qlc
      image: ...
      # As before
      mount: the_path/to_exercise
      # After the prefix as before
      cmd: qlc_wrap /exercise/run.sh

    qlc:
      # The command to produce QLC json
      cmd: python -m qlcpy --json submitted.py
      # Files having relevant content to see while answering the questions
      files:
        - submitted.py
