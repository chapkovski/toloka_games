_Philipp Chapkovski_
# _"Interactive experiments in Toloka"_


# JS and HTML for integrating Toloka and oTree

The integration of oTree and Toloka in its essence consists in adding a toloka assignment id in a form of url query parameter to an url that user clicks to reach the running oTree server (that points to either a waiting room or active session). So let's assume that your oTree session link looks like:

```html
http://my-study-link.herokuapp.com/join/abcdefg
```
which is a standard format for session-wide links in oTree. The provided JavaScript (JS) code when a user accepts the assignment, will automatically add the current assignment id in a following format:
```html
http://my-study-link.herokuapp.com/join/abcdefg?participant_label=ASSIGNMENT_ID
```
where `ASSIGNMENT_ID` will be substituted with an actual assignment id. This will assigns the assignment id to a participant label on oTree server side. Using this id will allow to retrieve any information related this assignment, including user id. That allows to automatically process variable payoffs based on a participant decision, and pay them in a form of bonus.

## Project creation

When a new project is created, its interface for a final user (study participant) can be built either by using a combination of html, css and JavaScript, or using the Toloka interface builder specification ([see more here](https://toloka.ai/ru/docs/template-builder/index.html?lang=en)). The interface builder does not allow passing the assignment information to the external link, so in order to integrate Toloka with oTree, it is necessary to choose 'HTML/JS/CSS' option, and insert the corresponding files either from `standard` or `timed` subfolders to the corresponding sections  (content of `project.css` to 'css' section, content of `project.html` to `html` section, and content of `project.js` to `js` section.)
![example of a new project](./img/new_project.png)


## Input and output fields

Toloka projects use a combination of templates (built with either interface builder or html), and input and output fields. The input fields are variable data that can vary from one study ('pool' in Toloka terminology) to another. They are injected in the template in the place where the field name in a corresponding place is used in curvy brackets. Thus if as an input field called `session_url` there is a link pointing to an active oTree session, and the completion code that confirms that participant indeed completed the study is collected as an output field `otree_code` the html may look like that:

```HTML
<div>
  Please click  <a href={{session_url}}>the following link</a> to start the study.
</div>

<div>
  {{field type="input" name="otree_code" placeholder="Please insert the completion code"}}
</div>

```
and the task file in a TSV (tab-separated values) format will look like that:

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |


There is one input field for task specification file: the field is called `session_url` and it refers to the session-wide link
in oTree server. The output code (`otree_code`) is the code that we ask them to fill in upon the study completion.

![input and output fields standard](./img/normal_data_spec.png)


## Timed projects
