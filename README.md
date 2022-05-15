# The 3 Equation Model Maker
Welcome to the 3 Equation Model Maker, by Neil Majithia
The app is hosted here: https://share.streamlit.io/nevadam/3equationmodelmaker/main/Client.py 

## Version: **Alpha 5.0**

### Changelog: 

#### Additions:
* Implemented Central Bank Credibility option
* Included Expected Inflation column

#### Updates / Bug Fixes:
* Fixed PC simulation in supply-side shocks

The old simulation ended up with a moving PC in period 5 despite expected inflation not changing, and had some other errors in supply side shocks.
* Cleaned PC curve drawer

The function for drawing the PC curves was bloated with loads of unnecessary conditions. When first writing it I probably did it to make it easier to visualise what I was doing, but I think it actually led to a lot of the errors in simulation and made the processing of the simulation take way longer
* Cleared some ambiguity in simulator functions

Specifically with CB responses in the simulator, it was often unclear why certain inputs were being used. Now, it's a little easier to follow - I want the code to be a decent learning aid too (idea is to think about actor behaviour as some sort of algorithm) and to do that it needs way less ambiguity
* Misc Bug Fixes

Some other boring bugs that I found, or botched bits of code, have been rewritten.

## Description
The aim of this program is to plot the exact state of the macroeconomy at any time period in a simulated shock.
It's a reconstruction of the Carlin & Soskice macroeconomic simulator (the excel simulator in the folder), built on their work on the 3 equation model.

The simulator (**Simulator.py**) outputs a numerical database that is translated into the model via my modelmaker  (**ModelMaker.py**)code. This is all hosted on a streamlit web app (**Client.py**).

This is still a work in progress, and currently I am working on implementing features to make it more of a learning/teaching aid. The streamlit site is a proof of concept - behind the scenes I'm learning how to turn this into a fully functioning web app.

Planned Updates to Streamlit site:
* ~~Impulse Response Functions - Alpha3~~
* ~~More columns (e.g. nom rates, q, expectations?) - Alpha4~~
* ~~Inclusion of anchored expectations and Central Bank Credibility - Alpha5~~
* Introduce POIs of the model (points A, B, C) - Alpha6
* Closed Economy - Beta1

After beta release work will be put into migration to a new web app based on Django/React/Something else.

Post release updates will include open economies with fixed rates - with fiscal policy and without

Report issues, suggestions, bugs etc in the issues tab on github, or email me at neil.majithia@live.co.uk 

-NM
