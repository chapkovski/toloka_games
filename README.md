_Philipp Chapkovski_
# _"Interactive experiments in Toloka"_

## Contents:

This repository contains a code of oTree games (Public good game, Dictator game, Rock-Scissors-Paper etc) plus a few extra modules.

All the games are created with oTree version [3.4.0](https://otree.readthedocs.io/en/self/) (so called [`self`](https://otree.readthedocs.io/en/self/)).

The extra modules are the following (all of them have their own separate README files, please refer to them for details):
- `toloka_front`: a piece of html/css/js code for Toloka projects to be able to pass Toloka assignment id to oTree. It includes both standard and timed versions (see the paper.)
- `paymodule`: The code to bulk process the payments  using assignments ids (obtained at the previous step) and oTree payoffs. It also includes the code for assigning skills (aka qualifications in mTurk terminology), that can be used later to filter out participants. 
- `scraper`: a small piece of code using which the data about online audience and user profiles from Toloka. 


All other folders are just oTree modules. To make the oTree project running in this folder just type 'otree devserver' (or 'otree prodserver' for production mode. For production mode read the [documentation](https://otree.readthedocs.io/en/self/server/intro.html) first. )

The folders are the following (in alphabetic order):
- `basicq`: a one page survey that was used in three platforms (mTurk, Prolific and Toloka) for measuring the arrival time (see introductory section of the paper. )
- `blocker`: a one-page app which contains a page that announces that people are blocked due to inactivity. 
- `dg`: a simple dictator game (which is preceded by a real effort task, which code is located in `ret` folder: see a corresponding section of the paper, where people are matched into dictator-recipient role depending on their efficiency at the real effort task.)
- `fullq`: the questionnaire for the large-scale survey of Russian speaking tolokers (see the corresponding section of the paper).
- `intro_matcher`: an intro page/app for the interactive games (Public Good Game/PGG, Rock-Scissors-Paper/RSP/ and Real effort task+Dictator game/ret+dg). It collects the user agent, arrival time and informs people that they may be blocked from the study if they are inactive (or also due to inactivity of other group members).
- `last`: a common last page for a set of interactive games. Only those participants who are eligible for payments finish there (thus those who are not blocked due to inactivity). It includes two pages: 'Last' (for normal endings), and `BlockedByOthers` for those who are forcefully ended the game because either their partner was blocked, or we were not able to match them within 90 seconds after arrival to the matching stage. 
- `matcher`: a common  waiting page for interactive games where people are matched into the groups. If they are not matched within a certain time (90 seconds in this particular study), they are redirected to the `BlockedByOthers` page (see `last` app description).
- `public goods`: a simple public good game for 3 participants and 10 rounds.
- `q`: a common post-experimental survey for a set of interactive games (pgg, dg+ret, rsp).
- `ret`: real effort task stage for ret+dg game (see a corresponding section in the paper). The task was to count the number of 0s in the matrix of numbers. They have to do as many tasks as possible within 2 minutes (adjustable via `settings -> ret_duration` parameter).
- `rsp`: a rock-scissors-paper game for 10 rounds.


