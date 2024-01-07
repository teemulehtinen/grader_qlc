# Follow up questions about the submitted program code

This is a mooc-grared exercise configuration and instruction to create 
questionnaires that ask about details of the student's program, which they have
submitted to a related programming exercise.

#### Configuration of the related programming exercise

See https://github.com/teemulehtinen/grader_qlc/ for how to augment the
grading container and configure the `qlc_wrap` tool. The result runs program
analysis that append invisible questionnaire data to the exercise feedback.

#### Creating the questionnaire about the submitted program

The following examples are from an RST based material. If you manage the HTML
and congifuration YAMLs in an other way, dig in to the required a-plus docs.

1. Copy the directory `aplus_followups` to your course as e.g.
   `/exercises/followups`.
2. Copy the `followups.js` to your static files as e.g. `_static/followups.js`
   and link chapter HTML to it in e.g. `_templates/layout.html`:
   ```html
   <script src="{{ pathto('_static/followups.js', 1) }}" data-aplus></script>
   ```
3. Create a new exercise that is **directly after** the augmented programming
   exercise **in a chapter** and mark it with the attribute `data-aplus-ajax`:
   ```rst
   Submit the programming assignment
   ---------------------------------
   .. submit:: hello_world 75
     :config: exercises/hello_world/config.yaml

   Follow up questions
   -------------------
   .. submit:: followup 15
     :ajax:
     :config: exercises/followups/config.yaml
   ```

## Removing the follow up questions

For each exercise having follow ups:
* In `config.yaml`, delete the current `image` and `cmd` lines
  and restore the commented out versions.
* Still in `config.yaml`, remove the `qlc` block completely.
* In the exercise `RST`:s, remove the follow up section,
  which includes the `..submit: followup` directive.

Clean up the common resources:
* In `_templates/layout.html`, remove the `followups.js` line.
* Delete `_static/followups.js`.
* Delete the directory `exercises/followups`.
