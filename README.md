# The 3 Equation Model Maker
Welcome to the 3 Equation Model Maker, by Neil Majithia
The app is hosted here: https://share.streamlit.io/nevadam/3equationmodelmaker/main/Client.py 

Version: alpha 3.05
Changelog: laid foundations for implementation of rational expectations


The aim of this program is to plot the exact state of the economy at any time period of a simulated shock.
It's a reconstruction of the Carlin & Soskice macroeconomic simulator (the excel simulator in the folder), built on their work on the 3 equation model.
The simulator (**Simulator.py**) outputs a numerical database that is translated into the model via my modelmaker  (**ModelMaker.py**)code. This is all hosted on a streamlit web app (**Client.py**).

This is still a work in progress, and currently I am working on implementing features to make it more of a learning/teaching aid. The streamlit site is a proof of concept - behind the scenes I'm learning Django to turn this into a fully functioning web app.

Planned Updates to Streamlit site:
* ~~Impulse Response Functions - Alpha3~~
* More columns (e.g. ~nom rates, q,~ expectations?) - Alpha4
* Inclusion of rational expectations and Central Bank Credibility - Alpha5
* Introduce POIs of the model (points A, B, C) - Alpha6
* Closed Economy - Beta1
After beta release work will be put into migration to a new web app based on Django/React
Post release updates will include open economies with fixed rates - with fiscal policy and without

Report issues, suggestions, bugs etc in the issues tab on github, or email me at neil.majithia@live.co.uk 

-NM
