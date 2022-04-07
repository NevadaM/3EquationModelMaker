from multiprocessing.connection import wait
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from re import template
import streamlit as st

import Simulator
import ModelMaker


###########################################

st.title('The Macroeconomic Simulator')
st.caption('by Neil Majithia')
st.text('')
st.text('Version: Alpha 2       neil.majithia@live.co.uk')
st.write('https://github.com/NevadaM/3EquationModelMaker')
st.text('')
st.write('''Welcome to the alpha2 version of the three equation model maker. 
At the current stage, this simulator only models open economies with flexible 
exchange rates. Planned updates are as follows: Impulse Response Function
addition, Closed Economy support, more columns in numerical data to simplify 
learning, and aesthetic updates''')


with st.sidebar.form('Options'):
    st.header('Options')
    submitted = st.form_submit_button('Click here to Simulate')
    tempinput = st.radio('Shock Duration: ', ['Temporary', 'Permanent'])
    sizeinput = st.number_input('Shock Size %: ', min_value=-20, max_value=20, value=0)
    typeinput = st.radio('Shock Type: ', ['Supply', 'Demand', 'Inflationary'])
    rstarinput = st.number_input('World Real Interest Rate (r*) %: ', min_value=0.0, value=3.0)
    piTinput = st.number_input('Target Inflation Rate (piT): ', min_value=0.0, value=2.0, step=0.1)
    alphainput = st.number_input('Inflation Sensitivity to Output Gap (alpha): ', min_value=0.0, value=1.0, step=0.01)
    betainput = st.number_input('Central Bank Inflation bias (beta): ', min_value=0.0, value=1.0, step=0.01)
    ainput = st.number_input('Expenditure Sensitivity to Real Interest Rate (a): ', min_value=0.0, value=0.75, step=0.01) 
    binput = st.number_input('Expenditure Sensitivity to Real Exchange Rate (b): ', min_value=0.01, value=0.1, step=0.01)

    
    st.sidebar.write('Reload the page to return default settings')
    

if submitted:
    if tempinput == 'Temporary':
        temporary = True
    else:
        temporary = False

    with st.spinner('Simulating and Modelling...'):
        sleep(2)
        sim = Simulator.Simulator(rstar=rstarinput, alpha=alphainput, beta=betainput, a=ainput, b=binput, piT=piTinput)
        if typeinput == 'Supply':
            df = sim.SupplyShock(size= (sizeinput), temporary=temporary)
            model = ModelMaker.ModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=False, supplyshock=True, 
            worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
            expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
            worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        elif typeinput == 'Demand':
            df = sim.DemandShock(size= (sizeinput), temporary=temporary)
            model = ModelMaker.ModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=True, 
            worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
            expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
            worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        elif typeinput == 'Inflationary':
            if not temporary:
                st.warning('Can\'t have a permanent inflation shock, here is temp instead ')
            st.info('This is the same as a temporary supply shock in the opposite direction')
            df = sim.SupplyShock(size=(-1 *  (sizeinput)), temporary=True)
            model = ModelMaker.ModelMaker(df, shocksizepct=(-1 *  (sizeinput)), temporary=True, demandshock=False, inflationshock=True, 
            worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
            expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
            worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        st.success('Complete!')

    st.dataframe(df)

    st.header('Summary')
    model.ThreeEquationsOverTime()

    st.header('Diagrams in a Specific Period')
    plist=[]
    for i in range(20):
        plist.append(i + 1)

    periodinput = st.select_slider('Choose a period: ', plist)
    model.ThreeEquationsPeriod(periodinput)

else:
    st.info('Choose your options in the sidebar and click the button at the top for your output')


