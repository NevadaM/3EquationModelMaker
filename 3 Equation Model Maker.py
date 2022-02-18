import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from re import template
#from google.colab import files
#import easygui

def DataCleaning(filepath):
  data = pd.read_excel(filepath)
  data = data.fillna(0)
  data[['Output gap', 'Growth', 'Inflation', 'Lending nom. i.r.', 'Lending real i.r.']] *= 100
  data = data.round(3)
  return data

class ModelMaker():
  ###take data, parameters as input and return full model simulation
  ###want output to be a list of subplots, indexed by period, showing the line in each period

  def __init__(self, df, shocksizepct=3, temporary=True, demandshock=True, supplyshock=False, inflationshock=False,
               flexiblerate=True, worldrate=3, inflationsensitivitytooutputgap=1, expendituresensitivitytointerestrate=0.75, CBcredibility=1,
               expendituresensitivitytorealer=0.1, worldinflationtarget=2, domesticinflationtarget=2, CBbeta=1,
               taxrate=0.2, publicexpenditurepct=0.2, publicdebt=0, equilibriumrealer=1, equilibriumnomer=1, equilibriumoutput=100):

               self.df = df
               self.shocksize = shocksizepct
               self.temporary = temporary
               self.multiplier = (0.01 * self.shocksize) + 1
               self.demandshock = demandshock
               self.supplyshock = supplyshock
               self.inflationshock = inflationshock
               self.flexiblerate = flexiblerate
               self.rstar = worldrate
               self.alpha = inflationsensitivitytooutputgap
               self.a = expendituresensitivitytointerestrate
               self.CBcredibility = CBcredibility
               self.b = expendituresensitivitytorealer
               self.adb = expendituresensitivitytorealer * 100
               self.worldinflationtarget = worldinflationtarget
               self.piT = domesticinflationtarget
               self.beta = CBbeta
               self.t = taxrate
               self.publicexpenditurepct = publicexpenditurepct
               self.publicdebt = publicdebt
               self.qbar = equilibriumrealer
               self.ebar = equilibriumnomer
               self.ye = equilibriumoutput
               self.A = self.ye + (self.a * self.rstar) - (self.b * self.qbar)
               self.adA = self.ye + (self.a * self.rstar) - (self.adb * self.qbar)

               self.x = np.linspace(95, 105, 11)

               if self.supplyshock and not self.temporary:
                 self.newye = self.ye * self.multiplier


  def ISCurve(self, period, only=True):
    #y = A - a r + b q
    #use last period's r, q, any new A
    #if self.demandshock == False:
    #  q = self.qbar
    #  r = self.rstar
    #  A = self.A

    #else:
    periodslice = self.df.loc[self.df['Periods'] == period]
    a = self.a
    b = self.b
    if period < 5:
      q = self.qbar
      r = self.rstar
      A = self.A
    else:
      lastperiodslice = self.df.loc[self.df['Periods'] == (period-1)]
      q = lastperiodslice['Real exchange rate'].values[0]
      r = lastperiodslice['Lending real i.r.'].values[0]
      A = periodslice['GDP'].values[0] + (a * r) - (b * q)

    r = []
    for i in self.x:
      r.append(round((A - i + (b * q)) / a, 2))

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(
          x=self.x, y=r, name='IS Curve', mode='lines', line={'color': 'blue'}
      ))
      fig1.update_layout(template='plotly_white', title=f'IS Curve - Period: {period}', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Real lending rate r', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.rstar)
      fig1.show()
    else:
      return r

  def RXResponses(self, only=True):
    #this is making rx from visible central bank actions
    ys = []
    for yentry in self.df['GDP']:
      ys.append(yentry)
    rs = [self.rstar]
    for rentry in self.df['Lending real i.r.'][:-1]:
      rs.append(rentry)

    if only:
      fig1 = go.Figure(data=[
                      go.Scatter(x=ys, y=rs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'square'})
                        ],
                       )
      fig1.update_layout(template='plotly_white', title='POIs', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Real lending rate r', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.rstar)
      fig1.show()
    else:
      return ys, rs

  def RXCurve(self, only=True):
    r = []
    for i in self.x:
      r.append(((self.ye - i) / ((self.a) + (self.b / (1 - (1 / (1 + ((self.alpha ** 2) * self.beta))))))) + self.rstar)

    newr=[]
    if self.supplyshock and not self.temporary:
      for i in self.x:
        newr.append(((self.newye - i) / ((self.a) + (self.b / (1 - (1 / (1 + ((self.alpha ** 2) * self.beta))))))) + self.rstar)

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(
          x=self.x, y=r, name='RX Curve', mode='lines', line={'color': 'red'}
      ))
      if self.supplyshock and not self.temporary:
        fig1.add_trace(go.Scatter(
          x=self.x, y=newr, name='New RX Curve', mode='lines', line={'color': 'maroon'}
          ))
        fig1.add_vline(self.newye, line={'color': 'lightgrey'})
      fig1.update_layout(template='plotly_white', title='RX Curve', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Real lending rate r', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye, line={'color': 'lightgrey'})
      fig1.add_hline(self.rstar)
      fig1.show()
    else:
      return r, newr



  def ISRXDiagram(self, period):
    IS = self.ISCurve(period, only=False)
    RXys, RXrs = self.RXResponses(only=False)
    RXCurvers, NewRXCurvers = self.RXCurve(only=False)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
          x=self.x, y=IS, name='IS Curve', mode='lines', line={'color': 'blue'}
      ))
    fig1.add_trace(go.Scatter(
          x=self.x, y=RXCurvers, name='RX Curve', mode='lines', line={'color': 'red'}
      ))
    if self.supplyshock and not self.temporary and period >= 5:
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewRXCurvers, name='New RX Curve', mode='lines', line={'color': 'maroon'}
          ))
        fig1.add_vline(self.newye, line={'color': 'lightgrey'})
    fig1.add_trace(go.Scatter(x=RXys, y=RXrs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'square'}))
    fig1.update_layout(template='plotly_white', title=f'IS-RX Diagram - Period: {period}', height=700, width=700, showlegend=True)
    fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
    fig1.update_yaxes(title_text='Real lending rate r', showline=True, linecolor='black', linewidth=1)
    fig1.add_vline(self.ye, line={'color': 'lightgrey'})
    fig1.add_hline(self.rstar, line={'color': 'lightgrey'})

    fig1.show()

  def ADCurve(self, period, only=True):
    #y = A - a r + b q
    #use last period's r, q, any new A
    #if self.demandshock == False:
    #  q = self.qbar
    #  r = self.rstar
    #  A = self.A

    #else:
    periodslice = self.df.loc[self.df['Periods'] == period]
    a = self.a
    b = self.adb
    if period < 5:
      q = self.qbar
      r = self.rstar
      A = self.adA
    else:
      lastperiodslice = self.df.loc[self.df['Periods'] == (period-1)]
      q = lastperiodslice['Real exchange rate'].values[0]
      r = lastperiodslice['Lending real i.r.'].values[0]
      A = periodslice['GDP'].values[0] + (a * r) - (b * q)

    q = []
    for i in self.x:
      q.append(round((A - i - (a * r)) / (b * -1), 2))

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(
          x=self.x, y=q, name='AD Curve', mode='lines', line={'color': 'green'}
      ))
      fig1.update_layout(template='plotly_white', title=f'AD Curve - Period: {period}', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Real exchange rate q', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.qbar)
      fig1.show()
    else:
      return q

  def ERPoints(self, only=True):
    ys = []
    for yentry in self.df['GDP']:
      ys.append(yentry)
    qs = []
    for qentry in self.df['Real exchange rate']:
      qs.append(qentry)

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(x=ys, y=qs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'hexagon'}))
      fig1.update_layout(template='plotly_white', title='POIs', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Real exchange rate q', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.qbar)
      fig1.show()
    else:
      return ys, qs


  def ADERUDiagram(self, period):
    AD = self.ADCurve(period, only=False)
    ERys, ERqs = self.ERPoints(only=False)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
          x=self.x, y=AD, name='AD Curve', mode='lines', line={'color': 'green'}
      ))
    fig1.add_trace(go.Scatter(x=ERys, y=ERqs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'hexagon'}))
    fig1.update_layout(template='plotly_white', title=f'AD-ERU Diagram - Period: {period}', height=700, width=700, showlegend=True)
    fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
    fig1.update_yaxes(title_text='Real exchange rate q', showline=True, linecolor='black', linewidth=1)
    fig1.add_hline(self.qbar, line={'color': 'lightgrey'})
    fig1.add_vline(self.ye, line={'color': 'violet'})
    if self.supplyshock and not self.temporary:
      fig1.add_vline(self.newye, line={'color': 'darkviolet'})

    fig1.show()

  def MRCurve(self, only=True):
    pi = []
    for i in self.x:
      pi.append(round(((self.ye - i) / (self.alpha * self.beta)) + self.piT, 2))

    newpi=[]
    if self.supplyshock and not self.temporary:
      for i in self.x:
        newpi.append(round(((self.newye - i) / (self.alpha * self.beta)) + self.piT, 2))

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(
          x=self.x, y=pi, name='MR Curve', mode='lines', line={'color': 'orange'}
      ))
      if self.supplyshock and not self.temporary:
        fig1.add_trace(go.Scatter(
          x=self.x, y=newpi, name='New RX Curve', mode='lines', line={'color': 'tan'}
          ))
        fig1.add_vline(self.newye, line={'color': 'lightgrey'})
      fig1.update_layout(template='plotly_white', title='MR Curve', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.piT)
      fig1.show()
    else:
      return pi, newpi

  def PhillipsCurve(self, period, only=True):
    if period == 1:
      piE = self.piT
    else:
      lastperiodslice = self.df.loc[self.df['Periods'] == (period-1)]
      piE = lastperiodslice['Inflation'].values[0]

    pi = []
    if not self.supplyshock and not self.inflationshock or period < 5:
      for i in self.x:
        pi.append(round((piE + (self.alpha * (i - self.ye))), 2))
      #print('not working 1 ')
    elif self.inflationshock:
      for i in self.x:
        if period == 5:
          pi.append(round((piE + (self.alpha * (i - self.ye + self.shocksize))), 2))
        else:
          pi.append(round((piE + (self.alpha * (i - self.ye))), 2))
      #print('works')
    else:
      for i in self.x:
        pi.append(round((piE + (self.alpha * (i - self.newye))), 2))
      #print('not working 2')

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(
          x=self.x, y=pi, name='Phillips Curve', mode='lines', line={'color': 'purple'}
      ))
      fig1.update_layout(template='plotly_white', title=f'Phillips Curve - Period: {period}', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye, line={'color': 'lightgrey'})
      fig1.add_hline(self.piT, line={'color': 'lightgrey'})
      if self.supplyshock and not self.temporary:
        fig1.add_vline(self.newye, line={'color': 'lightgrey'})
      fig1.show()
    else:
      return pi

  def PhillipsCurvePoints(self, only=True):
    ys = []
    for yentry in self.df['GDP']:
      ys.append(yentry)

    pis = []
    for pientry in self.df['Inflation']:
      pis.append(pientry)

    if only:
      fig1 = go.Figure()
      fig1.add_trace(go.Scatter(x=ys, y=pis, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'triangle-up'}))
      fig1.update_layout(template='plotly_white', title='Points', height=700, width=700, showlegend=True)
      fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
      fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='black', linewidth=1)
      fig1.add_vline(self.ye)
      fig1.add_hline(self.piT)
      fig1.show()
    else:
      return ys, pis


  def MRPCDiagram(self, period):
    PC = self.PhillipsCurve(period, only=False)
    PCpointys, PCpointpis = self.PhillipsCurvePoints(only=False)
    MR, NewMR = self.MRCurve(only=False)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=PCpointys, y=PCpointpis, name='POIs', mode='markers',
                               marker={'color': '#000000', 'size': 7, 'symbol': 'triangle-up'}))
    fig1.add_trace(go.Scatter(
          x=self.x, y=PC, name='Phillips Curve', mode='lines', line={'color': 'purple'}
      ))
    fig1.add_trace(go.Scatter(
          x=self.x, y=MR, name='MR Curve', mode='lines', line={'color': 'orange'}
      ))
    if self.supplyshock and not self.temporary and period >= 5:
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewMR, name='New MR Curve', mode='lines', line={'color': 'tan'}
          ))
        fig1.add_vline(self.newye, line={'color': 'lightgrey'})
    fig1.update_layout(template='plotly_white', title=f'MR-PC Diagram - Period: {period}', height=700, width=700, showlegend=True)
    fig1.update_xaxes(title_text='Output y', showline=True, linecolor='black', linewidth=1)
    fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='black', linewidth=1)
    fig1.add_vline(self.ye)
    fig1.add_hline(self.piT)
    fig1.show()


  def ThreeEquationsPeriod(self, period):
    IS = self.ISCurve(period, only=False)
    RXys, RXrs = self.RXResponses(only=False)
    RXCurvers, NewRXCurvers = self.RXCurve(only=False)
    AD = self.ADCurve(period, only=False)
    ERys, ERqs = self.ERPoints(only=False)
    PC = self.PhillipsCurve(period, only=False)
    PCpointys, PCpointpis = self.PhillipsCurvePoints(only=False)
    MR, NewMR = self.MRCurve(only=False)

    fig1 = make_subplots(rows=3, cols=1, vertical_spacing=0.05, shared_xaxes=True,
                         subplot_titles=['IS-RX Diagram', 'AD-ERU Diagram', 'MR-PC Curve'])

    fig1.add_trace(go.Scatter(
          x=self.x, y=IS, name='IS Curve', mode='lines', line={'color': 'blue'}
      ), row=1, col=1)
    fig1.add_trace(go.Scatter(
          x=self.x, y=RXCurvers, name='RX Curve', mode='lines', line={'color': 'red'}
      ), row=1, col=1)
    fig1.add_trace(go.Scatter(x=RXys, y=RXrs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'square'}
      ), row=1, col=1)
    fig1.add_trace(go.Scatter(
          x=self.x, y=AD, name='AD Curve', mode='lines', line={'color': 'green'}
      ), row=2, col=1)
    fig1.add_trace(go.Scatter(x=ERys, y=ERqs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'hexagon'}
      ), row=2, col=1)
    fig1.add_trace(go.Scatter(
          x=self.x, y=PC, name='Phillips Curve', mode='lines', line={'color': 'purple'}
      ), row=3, col=1)
    fig1.add_trace(go.Scatter(
          x=self.x, y=MR, name='MR Curve', mode='lines', line={'color': 'orange'}
      ), row=3, col=1)
    fig1.add_trace(go.Scatter(x=PCpointys, y=PCpointpis, name='POIs', mode='markers',
                               marker={'color': '#000000', 'size': 7, 'symbol': 'triangle-up'}
      ), row=3, col=1)

    if self.supplyshock and not self.temporary and period >= 5:
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewRXCurvers, name='New RX Curve', mode='lines', line={'color': 'maroon'}
          ), row=1, col=1)
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewMR, name='New MR Curve', mode='lines', line={'color': 'tan'}
          ), row=3, col=1)
        fig1.add_vline(self.newye, row=2, line={'color': 'darkviolet'})
    fig1.add_vline(self.ye, row=[1, 3], line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_vline(self.ye, row=2, line={'color': 'violet', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.rstar, row=1, col=1, line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.qbar, row=2, col=1, line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.piT, row=3, col=1, line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.update_layout(template='plotly_white', title=f'Period: {period}', height=1000, width=500, margin={'l': 20, 'r': 20, 'b': 25, 't': 35},
                       xaxis_showticklabels=True, xaxis2_showticklabels=True, xaxis3_showticklabels=True,
                       yaxis_showticklabels=True, yaxis2_showticklabels=True, yaxis3_showticklabels=True)
    fig1.update_xaxes(showline=True, linecolor='darkgray', linewidth=1)
    fig1.update_yaxes(title_text='Real Interest Rate r', showline=True, linecolor='darkgray', linewidth=1, row=1, col='all')
    fig1.update_yaxes(title_text='Real Exchange Rate q', showline=True, linecolor='darkgray', linewidth=1, row=2, col='all')
    fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='darkgray', linewidth=1, row=3, col='all')
    fig1.update_yaxes(showline=True, linecolor='darkgray', linewidth=1)
    fig1.show()


  def ThreeEquationsOverTime(self):
    fig1 = make_subplots(rows=3, cols=4, vertical_spacing=0.05, horizontal_spacing=0.05, shared_xaxes=True, shared_yaxes=True,
                         row_titles=['IS-RX Diagram', 'AD-ERU Diagram', 'MR-PC Curve'],
                         column_titles=['Period1 / Equilibrium', 'Period5 / Shock', 'Period6', 'Period19 / New Equilibrium'])

    RXys, RXrs = self.RXResponses(only=False)
    RXCurvers, NewRXCurvers = self.RXCurve(only=False)
    ERys, ERqs = self.ERPoints(only=False)
    PCpointys, PCpointpis = self.PhillipsCurvePoints(only=False)
    MR, NewMR = self.MRCurve(only=False)

    fig1.add_trace(go.Scatter(x=RXys, y=RXrs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'square'}
      ), row=1, col='all')
    fig1.add_trace(go.Scatter(x=ERys, y=ERqs, name='POIs', mode='markers',
                                 marker={'color': '#000000', 'size': 7, 'symbol': 'hexagon'}
      ), row=2, col='all')
    fig1.add_trace(go.Scatter(x=PCpointys, y=PCpointpis, name='POIs', mode='markers',
                               marker={'color': '#000000', 'size': 7, 'symbol': 'triangle-up'}
      ), row=3, col='all')

    periods = [1, 5, 6, 19]
    for period in periods:
      IS = self.ISCurve(period, only=False)
      AD = self.ADCurve(period, only=False)
      PC = self.PhillipsCurve(period, only=False)

      column = periods.index(period) + 1

      fig1.add_trace(go.Scatter(
          x=self.x, y=IS, name='IS Curve', mode='lines', line={'color': 'blue'}
      ), row=1, col=column)
      fig1.add_trace(go.Scatter(
          x=self.x, y=RXCurvers, name='RX Curve', mode='lines', line={'color': 'red'}
      ), row=1, col=column)
      fig1.add_trace(go.Scatter(
          x=self.x, y=AD, name='AD Curve', mode='lines', line={'color': 'green'}
      ), row=2, col=column)

      fig1.add_trace(go.Scatter(
          x=self.x, y=PC, name='Phillips Curve', mode='lines', line={'color': 'purple'}
      ), row=3, col=column)
      fig1.add_trace(go.Scatter(
          x=self.x, y=MR, name='MR Curve', mode='lines', line={'color': 'orange'}
      ), row=3, col=column)

      if self.supplyshock and not self.temporary and period >= 5:
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewRXCurvers, name='New RX Curve', mode='lines', line={'color': 'maroon'}
          ), row=1, col=column)
        fig1.add_trace(go.Scatter(
          x=self.x, y=NewMR, name='New MR Curve', mode='lines', line={'color': 'tan'}
          ), row=3, col=column)
        fig1.add_vline(self.newye, row=2, col=column, line={'color': 'darkviolet'})


    fig1.add_vline(self.ye, row='all', col='all', line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.rstar, row=1, col='all', line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.qbar, row=2, col='all', line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.add_hline(self.piT, row=3, col='all', line={'color': 'lightgrey', 'dash': 'solid', 'width': 1})
    fig1.update_layout(template='plotly_white', height=900, width=1600, margin={'l': 20, 'r': 20, 'b': 25, 't': 35},
                       xaxis_showticklabels=True, xaxis2_showticklabels=True, xaxis3_showticklabels=True, xaxis4_showticklabels=True,
                       xaxis5_showticklabels=True, xaxis6_showticklabels=True, xaxis7_showticklabels=True, xaxis8_showticklabels=True,
                       xaxis9_showticklabels=True, xaxis10_showticklabels=True, xaxis11_showticklabels=True, xaxis12_showticklabels=True,
                       yaxis_showticklabels=True, yaxis2_showticklabels=True, yaxis3_showticklabels=True, yaxis4_showticklabels=True,
                       yaxis5_showticklabels=True, yaxis6_showticklabels=True, yaxis7_showticklabels=True, yaxis8_showticklabels=True,
                       yaxis9_showticklabels=True, yaxis10_showticklabels=True, yaxis11_showticklabels=True, yaxis12_showticklabels=True)
    fig1.update_xaxes(showline=True, linecolor='darkgray', linewidth=1)
    fig1.update_yaxes(title_text='Real Interest Rate r', showline=True, linecolor='darkgray', linewidth=1, row=1, col='all')
    fig1.update_yaxes(title_text='Real Exchange Rate q', showline=True, linecolor='darkgray', linewidth=1, row=2, col='all')
    fig1.update_yaxes(title_text='Inflation pi', showline=True, linecolor='darkgray', linewidth=1, row=3, col='all')
    fig1.update_yaxes(showline=True, linecolor='darkgray', linewidth=1)
    #print(fig1.layout)
    fig1.show()


def Start():
  print()
  print('----------------------------------------------------')
  print('Welcome to the 3 Equation Model Maker, by Neil Majithia')
  print()
  print('The aim of this program is to plot the exact state of the economy at any time period of a simulated shock. \nIt requires the use of the Carlin & Soskice macroeconomic simulator, built on their fantastic work on the 3 equation model.')
  print('The simulator outputs impulse response functions and the numerical data behind them. The latter is used here, provided you run the simulator yourself and feed this program the output.')
  print('This is still a work in progress, and currently I am working on implementing non-default settings.')
  print('Thank you for using this program, I hope it\'s useful!')
  print('Direct all feedback to neil.majithia@live.co.uk')
  print('----------------------------------------------------')
  print()
  print('Please answer some questions about your simulator setup to initialise the model maker in the right way.')
  print('Firstly, you need to run the simulator with your choice of shock and settings. Go to the numerical results table and copy the first 20 periods\' entries and all column names, from \'Period\' to \'NIIP/GDP\'. ')
  print('Open a new excel spreadsheet and paste the results - but VALUES ONLY. This can be done by right clicking and choosing \'Values\' from the paste options section.')
  print('Save this new excel spreadsheet as SimOutput.xlsx, in an accessible location.')
  input('Once you\'re done with that, type anything into the box below and hit enter. You\'ll be taken to select your SimOutputFile. \n')
  #file = easygui.fileopenbox()
  file = 'C:\Users\neilm\OneDrive\Desktop\3 Equation Model Maker.py'
  data = DataCleaning(file)
  input('\nNow you\'ve uploaded your data, answer the next few questions corresponding to what your shock was. Make sure you answer completely in line with what you put in the simulator.\nType anything and hit enter to continue\n')
  size = input(' What is the size of the shock? Type as a percentage of GDP. Positive number = Positive shock. Negative number = Negative shock \n')
  shockduration = input('\n Is the shock temporary or permanent? \n If the shock is inflationary, it can only be temporary. \n Type 1 for temporary and 2 for permanent. \n')
  shocktype = input('\n What kind of shock is it? \n Type 1 for supply side, 2 for demand side and 3 for inflationary. \n')
  defaultsettings = input('\n Is the simulator set to default settings (other than the shocks)? \n Type 1 for yes, 2 for no. \n')
  if defaultsettings == '2':
    '\n non-default settings aren\'t supported yet'

  if shockduration == '1':
    if shocktype == '1':
      print(f'\nTemporary {size}% Supply Side Shock = {-int(size)}% Inflationary Shock')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=(-int(size)), temporary=True, demandshock=False, inflationshock=True)
    elif shocktype == '2':
      print(f'\nTemporary {size}% Demand Side Shock')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=int(size))
    elif shocktype == '3':
      print(f'{size}% Inflationary Shock')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=(int(size)), temporary=True, demandshock=False, inflationshock=True)

  elif shockduration == '2':
    if shocktype == '1':
      print(f'\nPermanent {size}% Supply Side Shock')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=(int(size)), temporary=False, demandshock=False, supplyshock=True)
    elif shocktype == '2':
      print(f'\nPermanent {size}% Demand Side Shock')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=int(size), temporary=False)
    elif shocktype == '3':
      print(f'\nCan\'t have a permanent {size}% Inflationary Shock, so here\'s a temporary one')
      print('Model has been saved as model')
      return ModelMaker(data, shocksizepct=(int(size)), temporary=True, demandshock=False, inflationshock=True)

def Help():
  print()
  print('-----------GUIDE--------------')
  print('The model maker can output individual lines, paths of points and full diagrams')
  print('It can also output the entire three equation model diagrams for any given period')
  print('Or, it can output the diagrams for the most important periods')
  print()
  print('Commands for Individual Lines:')
  print('model.ISCurve(period).................................IS Curve for a certain period')
  print('model.ADCurve(period).................................AD Curve for a certain period')
  print('model.PhillipsCurve(period)...........................Phillips Curve for a certain period')
  print('model.RXCurve().......................................RX Curve (if permanent supply shock, gives both old and new RX Curves)')
  print('model.MRCurve().......................................MR Curve (if permanent supply shock, gives both old and new MR Curves)')
  print()
  print('Commands for Paths of Points:')
  print('model.RXResponses()...................................Plots movement of real interest rate on the IS RX Diagram')
  print('model.ERPoints()......................................Plots movement of exchange rate on AD ERU Diagram')
  print('model.PhillipsCurvePoints()...........................Plots movement of inflation rate on MR PC Diagram')
  print()
  print('Commands for Full Diagrams:')
  print('model.ISRXDiagram(period).............................IS RX Diagram for a certain period')
  print('model.ADERUDiagram(period)............................AD ERU Diagram for a certain period')
  print('model.MRPCDiagram(period).............................MR Phillips Curve Diagram for a certain period')
  print()
  print('Commands for full three diagrams: ')
  print('model.ThreeEquationsPeriod(period)....................Position of all lines for a certain period')
  print('model.ThreeEquationsOverTime()........................Position of all lines for equilibrium, shock, response and new equilibrium')
  print()
  print('To use one of these functions, just type exactly what is on the left hand side, replacing period with whatever is your choice.')
  print('e.g. model.ThreeEquationsPeriod(1) for period 1')
  print()
  print('Other Commands: ')
  print('Start()...............................................Restart with new data')
  print('Help()................................................Print this message again')
  print()
  print('Any further questions/troubleshooting, contact neil.majithia@live.co.uk')


model = Start()
Help()
