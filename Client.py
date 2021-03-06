from multiprocessing.connection import wait
from time import sleep
import pandas
import matplotlib.pyplot
import plotly.express
import plotly.graph_objects
import numpy
from plotly.subplots import make_subplots
from re import template
import streamlit as st

from Simulator import Simulator as OEsim
from ModelMaker import OEModelMaker, CEModelMaker
import ImpulseResponseMaker
from ClosedEconomySim import CEsim


###########################################

st.title('The Macroeconomic Simulator')
st.caption('by Neil Majithia')
st.text('')
st.text('Version: BETA 1.0      neil.majithia@live.co.uk')
st.write('https://github.com/NevadaM/3EquationModelMaker')
st.text('')
st.write('''Welcome to the Beta1 version of the three equation model maker. 
See the GitHub page for info. Planned updates can be viewed in the github readme. If you have 
any issues, get in touch on the github issues tab, or via the email address above.''')


with st.sidebar.form('Options'):
    st.header('Create your shock')
    submitted = st.form_submit_button('Click here to Simulate')
    econinput = st.radio('Type of Economy: ', ['Closed Economy', 'Open Economy with Flexible ER'])
    tempinput = st.radio('Shock Duration: ', ['Temporary', 'Permanent'])
    sizeinput = st.number_input('Shock Size %: ', min_value=-20, max_value=20, value=3)
    if sizeinput == 0:
        st.error("Shock Size can't be 0")
    typeinput = st.radio('Shock Type: ', ['Supply', 'Demand', 'Inflationary'])
    credinput = st.number_input('Credibility of Central Bank', min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    rstarinput = st.number_input('World Real Interest Rate (r*) %: ', min_value=0.0, value=3.0)
    piTinput = st.number_input('Target Inflation Rate (piT): ', min_value=0.0, value=2.0, step=0.1)
    alphainput = st.number_input('Inflation Sensitivity to Output Gap (alpha): ', min_value=0.0, value=1.0, step=0.01)
    betainput = st.number_input('Central Bank Inflation bias (beta): ', min_value=0.0, value=1.0, step=0.01)
    ainput = st.number_input('Expenditure Sensitivity to Real Interest Rate (a): ', min_value=0.0, value=0.75, step=0.01) 
    binput = st.number_input('Expenditure Sensitivity to Real Exchange Rate (b): ', min_value=0.01, value=0.1, step=0.01)

    
    st.sidebar.write('Reload the page to return default settings')
    st.sidebar.write('Special Thanks to Alessandro Guarnieri')
    
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if submitted:
    st.session_state.submitted = True

if sizeinput == 0:
    st.error("Shock Size can't be 0 - please change it in the sidebar")

elif st.session_state.submitted:
    if tempinput == 'Temporary':
        temporary = True
    else:
        temporary = False

    with st.spinner('Simulating and Modelling...'):
        sleep(2)
        if econinput == 'Closed Economy':
            sim = CEsim(rstar=rstarinput, alpha=alphainput, beta=betainput, a=ainput, piT=piTinput, credibility=credinput)
        else: 
            sim = OEsim(rstar=rstarinput, alpha=alphainput, beta=betainput, a=ainput, b=binput, piT=piTinput, credibility=credinput)
        if typeinput == 'Supply':
            df = sim.SupplyShock(size= (sizeinput), temporary=temporary)
            if econinput == 'Closed Economy':
                model = CEModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=False, supplyshock=True, 
            rstar=rstarinput, inflationsensitivitytooutputgap=alphainput, 
            expendituresensitivitytointerestrate=ainput,
            domesticinflationtarget=piTinput, CBbeta=betainput)
            else:
                model = OEModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=False, supplyshock=True, 
                worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
                expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
                worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        elif typeinput == 'Demand':
            df = sim.DemandShock(size= (sizeinput), temporary=temporary)
            if econinput == 'Closed Economy':
                model = CEModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=True, supplyshock=False, 
                rstar=rstarinput, inflationsensitivitytooutputgap=alphainput, 
                expendituresensitivitytointerestrate=ainput,
                domesticinflationtarget=piTinput, CBbeta=betainput)
            else:
                model = OEModelMaker(df, shocksizepct= (sizeinput), temporary=temporary, demandshock=True, 
                worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
                expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
                worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        elif typeinput == 'Inflationary':
            if not temporary:
                st.warning('Can\'t have a permanent inflation shock, here is temp instead ')
            st.info('This is the same as a temporary supply shock in the opposite direction')
            df = sim.SupplyShock(size=(-1 *  (sizeinput)), temporary=True)
            if econinput == 'Closed Economy':
                model = CEModelMaker(df, shocksizepct= (-1 * sizeinput), temporary=True, demandshock=False, inflationshock=True, 
                rstar=rstarinput, inflationsensitivitytooutputgap=alphainput, 
                expendituresensitivitytointerestrate=ainput,
                domesticinflationtarget=piTinput, CBbeta=betainput)
            else:
                model = OEModelMaker(df, shocksizepct=(-1 *  (sizeinput)), temporary=True, demandshock=False, inflationshock=True, 
                worldrate=rstarinput, inflationsensitivitytooutputgap=alphainput, 
                expendituresensitivitytointerestrate=ainput, expendituresensitivitytorealer=binput, 
                worldinflationtarget=piTinput, domesticinflationtarget=piTinput, CBbeta=betainput)
        st.success('Complete!')

    IRMaker = ImpulseResponseMaker.ImpulseResponses(df, rstar=rstarinput, piT=piTinput)
    plist=[]
    for i in range(20):
        plist.append(i + 1)

    st.header('Numerical Results')
    st.dataframe(df)

    st.header('Impulse Response Functions')
    with st.expander('Expand to see Impulse Response Functions', expanded=False):
        IRMaker.GDP()
        IRMaker.Inflation()
        IRMaker.RealExchangeRate() if econinput == 'Open Economy with Flexible ER' else None
        IRMaker.RealInterestRate()    

    st.header('Three Equations - Key Periods')
    with st.expander('Expand to see 3 equation diagrams for 4 key periods of the timeline'):
        model.ThreeEquationsOverTime()

    st.header('Three Equation Diagrams for a Specific Period')
    with st.expander('Expand to choose a period of the timeline and see what the diagrams look like for it'):
        periodinput = st.select_slider('Choose a period: ', options=plist, value=1)
        model.ThreeEquationsPeriod(periodinput)

else:
    st.info('Choose your options in the sidebar and click the button at the top for your output')



