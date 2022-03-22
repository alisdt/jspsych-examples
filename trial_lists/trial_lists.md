Three ways to do trial lists
============================

Here I'm using "trial list" to mean a table that specifies the values (stimuli, durations etc.) for a set of trials. For example:

word | duration
--------|---------
MOUSE   | 250
RAT     | 500
CAPYBARA | 750


Imagine you've written your jsPsych code, everybody is happy with the ten trials that run. Then your supervisor (or reviewer) says to you, hey, you need more trials. Suddenly you want to run 50 trials. Cutting and pasting the trial definition suddenly doesn't look so great ....

Here are three ways to do trial lists in jsPsych. They all have their advantages and disadvantages which I'll discuss as we go.

A big JavaScript array
----------------------

You've probably already seen timeline variables, (ATFIXME: link) but here's a reminder.
Instead of writing out all your trials "longhand":

```javascript
// ATFIXME: untested
const trial1 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: "MOUSE",
    prompt: "If you like this word press <em>A</em>. If you don't like it press <em>L</em>.",
    stimulus_duration: 250
};
const trial2 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: "RAT",
    prompt: "If you like this word press <em>A</em>. If you don't like it press <em>L<em>.",
    stimulus_duration: 500
};
const trial3 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: "CAPYBARA",
    prompt: "If you like this word press <em>A</em>. If you don't like it press <em>L</em>.",
    stimulus_duration: 750
};
const timeline = [trial1, trial2, trial3];
```

you can combine them like so:

```javascript
// ATFIXME: untested
const trial_stimuli = [
    { stimulus: "MOUSE", duration: 250 },
    { stimulus: "RAT", duration: 500 },
    { stimulus: "CAPYBARA", duration: 750 }
];
const trial = {
    type: jsPsychHtmlButtonResponse,
    stimulus: jsPsych.timelineVariable("stimulus"),
    prompt: "If you like this word press <em>A</em>. If you don't like it press <em>L</em>.",
    stimulus_duration: jsPsych.timelineVariable("duration")
};
const timeline_trial = {
    timeline: [trial],
    timeline_variables: trial_stimuli
};
```

This is fine for a few trials, but what if you had 50, 100, or more? Ideally we'd move them somewhere that isn't in our main JavaScript code file.

Stimulus list in a JavaScript file
----------------------------------

We could move the timeline variables ("variables" in the example above) to another file.

Let's say this code:

```javascript
const variables = [
    { stimulus: "MOUSE", duration: 250 },
    { stimulus: "RAT", duration: 500 },
    { stimulus: "CAPYBARA", duration: 750 }
];
```

is moved to `stimulus_list.js`. Then all we need to do is include this before our main
experiment JavaScript file, in the HTML file, e.g.:

```html
<script src="stimulus_list.js"></script>
<script src="experiment.js"></script>
```

The browser reads these in order -- any variables defined are available in subsequent
JavaScript files.

What if you already have a CSV file with your trial list?
---------------------------------------------------------

You *could* convert your CSV to JSON (JavaScript Object Notation). This is a JavaScript object value on its own. There are lots of free online services which do this -- fine to use as long as your trial list doesn't contain any personal or confidential information. So this CSV:

ATFIXME: footnote

```python
import pandas as pd
df = pd.read_csv("example.csv")
df.to_json("example.json", orient="records")
```

```
stimulus,duration
MOUSE,250
RAT,500
CAPYBARA,750
```

would become this JSON:

```
[
    { stimulus: "MOUSE", duration: 250 },
    { stimulus: "RAT", duration: 500 },
    { stimulus: "CAPYBARA", duration: 750 }
]
```

Note that spaces and new lines are purely cosmetic in JavaScript so it may look a little different!

This is similar to the value given above, to use it in code we just have to add a variable name:

```javascript
const variables = [
    { stimulus: "MOUSE", duration: 250 },
    { stimulus: "RAT", duration: 500 },
    { stimulus: "CAPYBARA", duration: 750 }
];
```

Converting to JSON makes this approach feasible even for larger trial lists, but if you plan on keeping the authoritative copy in a spreadsheet, you'll have to convert it every time! So what about getting data direct from CSV?

Loading a CSV file
------------------

You can load a stimulus list directly from a CSV file, in the same folder as your
experiment. While nothing will be visibly different, behind the scenes the participant's
browser will make an extra request to the server to get the contents of the CSV file.

There's a JavaScript library called PapaParse which will both download the CSV file and parse it into a JavaScript object. This is the equivalent of the conversion from CSV discussed above, except that it's done automatically behind the scenes every time the experiment loads.

If your experiment uses [the CDN method of loading jsPsych](https://www.jspsych.org/7.2/tutorials/hello-world/#option-1-using-cdn-hosted-scripts), add this to your .html file before your experiment code:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.1/papaparse.min.js" integrity="sha512-EbdJQSugx0nVWrtyK3JdQQ/03mS3Q1UiAhRtErbwl1YL/+e2hZdlIcSURxxh7WXHTzn83sjlh2rysACoJGfb6g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
```

If your experiment uses its own copy of jsPsych (in other words, if you uploaded jsPsych to your server), download a compact copy of PapaParse
<a href="https://github.com/mholt/PapaParse/raw/master/papaparse.min.js" download>
from GitHub
</a>
and upload it to your server. Add this to your .html file before your experiment code:

```html
<script src="papaparse.min.js"></script>
```

The PapaParse documentation is here: [https://www.papaparse.com/](https://www.papaparse.com/).

Now that you've got through all that, it's relatively easy to load data! But there's one more thing to understand before we go ahead.

Promises
--------

