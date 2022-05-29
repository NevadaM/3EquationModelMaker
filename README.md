# The 3 Equation Model Maker
Welcome to the 3 Equation Model Maker, by Neil Majithia
The app is hosted here: https://share.streamlit.io/nevadam/3equationmodelmaker/main/Client.py 

## Version: **Alpha 5.5**

### Changelog: 

#### Additions:
* Finally implemented proper POIs of the model

I still don't like their implementation, but Plotly is being annoying and it might take a complete rework of my drawing functions to get it to do POIs the way I'd like them to be. Might need some more research because the only way I can think of getting that rework to work would increase processing by a sizeable amount for some reason.

#### Updates / Bug Fixes:
* Fixed Legend duplicates

The duplicates in the Legend were bugging me and making it borderline unreadable. This is better but the whole POI stuff is still unclear. The code for it is also kinda stupid.

* Changed x axis range

I've made the x axis range adaptive to the shock sizes themselves. It's still a hard coded ratio which could get annoying later, but that's a future problem I guess. 

* Misc cleaning

I've been able to speed this all up by changing some conditions around. Would love to clean out some more but I think some of the stuff will be useful for later iterations, like public expenditure stuff. Shame I know nothing about that stuff huh.

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
