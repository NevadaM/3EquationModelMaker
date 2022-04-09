from re import template
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

#import Simulator #for example dataframe

####Take df from simulator, create impulse response funcs using plotly
#get example df

#sim = Simulator.Simulator()
#df = sim.DemandShock(3, temporary=True)

class ImpulseResponses():

    def __init__(self, df, ye=100, rstar=3, piT=2, ebar=1):
        self.df = df
        self.ye = ye
        self.rstar = rstar
        self.piT = piT
        self.ebar = ebar


    def GDP(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df['Periods'], y = self.df['GDP'], 
            name='GDP', mode='lines+markers', line={'color': 'blue'}, marker={'color': 'purple'}
        ))
        fig.update_layout(
            template='plotly_white', title='GDP / y', 
            height=450, width=800
            )
        fig.update_xaxes(
            title_text='Periods', showline=True, 
            linecolor='black', linewidth=1
        )
        fig.update_yaxes(
            title_text='GDP (y)', showline=True, 
            linecolor='black', linewidth=1
        )

        fig.add_hline(self.ye)
        fig.show()
        #st.plotly_chart(fig1)

    def Inflation(self):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
            x=self.df['Periods'], y = self.df['Inflation'], 
            name='Inflation', mode='lines+markers', line={'color': 'blue'}, marker={'color': 'purple'}
            ))
        fig.update_layout(
            template='plotly_white', title='Inflation / pi', 
            height=450, width=800
            )
        fig.update_xaxes(
            title_text='Periods', showline=True, 
            linecolor='black', linewidth=1
        )
        fig.update_yaxes(
            title_text='Inflation (pi)', showline=True, 
            linecolor='black', linewidth=1
        )

        fig.add_hline(self.piT)
        fig.show()
        #st.plotly_chart(fig1)

    def RealInterestRate(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df['Periods'], y = self.df['Lending real i.r.'], 
            name='Interest Rate', mode='lines+markers', line={'color': 'blue'}, marker={'color': 'purple'}
        ))
        fig.update_layout(
            template='plotly_white', title='Interest Rate / r', 
            height=450, width=800
            )
        fig.update_xaxes(
            title_text='Periods', showline=True, 
            linecolor='black', linewidth=1
        )
        fig.update_yaxes(
            title_text='Interest Rate (r)', showline=True, 
            linecolor='black', linewidth=1
        )

        fig.add_hline(self.rstar)
        fig.show()
        #st.plotly_chart(fig1)

    def RealExchangeRate(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df['Periods'], y = self.df['Real exchange rate'], 
            name='Real Exchange Rate', mode='lines+markers', line={'color': 'blue'}, marker={'color': 'purple'}
        ))
        fig.update_layout(
            template='plotly_white', title='Real Exchange Rate / Q', 
            height=450, width=800
            )
        fig.update_xaxes(
            title_text='Periods', showline=True, 
            linecolor='black', linewidth=1
        )
        fig.update_yaxes(
            title_text='Real Exchange Rate (Q)', showline=True, 
            linecolor='black', linewidth=1
        )

        fig.add_hline(self.ebar)
        fig.show()
        #st.plotly_chart(fig1)
