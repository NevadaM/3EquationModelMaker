# The 3 Equation Model Maker
Welcome to the 3 Equation Model Maker, by Neil Majithia
The app is hosted here: https://share.streamlit.io/nevadam/3equationmodelmaker/main/Client.py 

## Version: **Beta 1**

### Changelog: 

#### Additions:
* CLOSED ECONOMY SIMULATION !

Finally implemented a closed economy simulator and a corresponding closed economy modeller. These take same structure and commands as their open economy counterparts so hopefully seamless implementation.

#### Updates / Bug Fixes:
* Fixed output gap weirdness for permanent supply shocks

Output gap was in comparison to the old equilibrium, which gave stupid numbers

* Fixed nom rate calculation

Was using the fisher equation in the wrong way, so nom rates weren't even close to correct. Will at some point need to address the zero lower bound.

* Fixed plotting issues for negative shocks

Probably the most stupid typo i've ever done, works fine now

* Fixed weird wavy AD curve

Early rounding in the function, I kept the rounding but only to 4 places, gives enough precision for a straight line

* Misc cleaning

Got rid of some unused parameters. Marginal improvement on memory use. I think I should target processing more - some conditions especially within the client could be cleaned. Working on the django site gives me a good chance to do it, esp with the use of requests. 

* Hotfix Beta 1.1

Added validation logic for when shock size = 0, and changed default shock size to 3

## Description
The aim of this program is to plot the exact state of the macroeconomy at any time period in a simulated shock.
It's a reconstruction of the Carlin & Soskice macroeconomic simulator (the excel simulator in the folder), built on their work on the 3 equation model.

The simulator (**Simulator.py**) outputs a numerical database that is translated into the model via my modelmaker  (**ModelMaker.py**)code. This is all hosted on a streamlit web app (**Client.py**).

This is still a work in progress, and currently I am working on implementing features to make it more of a learning/teaching aid. The streamlit site is a proof of concept - behind the scenes I'm learning how to turn this into a fully functioning web app.

Planned Updates to Streamlit site:
* ~~Impulse Response Functions - Alpha3~~
* ~~More columns (e.g. nom rates, q, expectations?) - Alpha4~~
* ~~Inclusion of anchored expectations and Central Bank Credibility - Alpha5~~
* ~~ Introduce POIs of the model (points A, B, C) - Alpha6 ~~
* ~~ Closed Economy - Beta1 ~~

After beta release work will be put into migration to a new web app based on Django/React/Something else.

Post release updates will include open economies with fixed rates - with fiscal policy and without

Report issues, suggestions, bugs etc in the issues tab on github, or email me at neil.majithia@live.co.uk 

-NM
