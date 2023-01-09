FROM apluslms/grade-python:math-3.9-4.5-4.5

ARG GRADE_QLC_VER=v1.0.0
ARG QLCPY_VER=1.0.9

RUN pip_install \
    # Manipulates grader output
    https://github.com/teemulehtinen/grader_qlc/archive/refs/tags/${GRADE_QLC_VER}.tar.gz \
    # Generates python questions
    qlcpy==${QLCPY_VER} \
 && find /usr/local/lib/python* -type d -regex '.*/locale/[a-z_A-Z]+' -not -regex '.*/\(en\|fi\|sv\)' -print0 | xargs -0 rm -rf \
 && find /usr/local/lib/python* -type d -name 'tests' -print0 | xargs -0 rm -rf
