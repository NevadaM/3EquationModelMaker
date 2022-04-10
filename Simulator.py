import pandas as pd
import numpy as np

#SO FAR, ONLY  open economy
#To make this a better learning tool, could add cols like expected inflation

###HELPER METHODS

def FindOptimumY(expectedinflation, ye=100, piT=2, alpha=1, beta=1):
    ###optimum y found using intersect of next period's PC, MR
    y = (((alpha * beta) * (piT - expectedinflation)) / (1 + ((alpha ** 2) * (beta)))) + ye
    return y

def FindResponse(optimumY, ye=100, a=0.75, b=0.1, alpha=1, beta=1, rstar=3):
    r = (((ye - optimumY) / ((a) + (b / (1 - (1 / (1 + ((alpha ** 2) * beta))))))) + rstar)
    return r

def InflationfromY(y, ye=100, alpha=1, beta=1, piT=2):
    pi = ((ye - y) / (alpha * beta)) + piT
    return pi

def NewQBarDemand(shocksize, ye=100, a=0.75, b=0.1, rstar = 3, qbar=0): #shouldn't be 1? confusing/conflicting
    multiplier = (0.01 * shocksize) + 1
    oldA = ye + (a * rstar) - ((b * 100) * qbar)
    newqbar = (ye + (a * rstar) - (multiplier * oldA)) / (b * 100)
    return newqbar

def NewQBarSupply(shocksize, ye=100, a=0.75, b=0.1, rstar=3, qbar=0):
    multiplier = (0.01 * shocksize) + 1
    A = ye + (a * rstar) - ((b * 100) * qbar)
    newqbar = ((multiplier * ye) + (a * rstar) - A) / (b * 100)
    return newqbar

###SIMULATOR

class Simulator():
    def __init__(self, periods=25, ye=100, rstar=3, alpha=1, beta=1, 
                a=0.75, b=0.1, piT=2, t=0.2):
        
        self.periods = periods
        self.ye = ye
        self.rstar = rstar
        self.alpha = alpha
        self.beta = beta
        self.a = a
        self.b = b
        self.piT = piT
        self.t = t
        
        self.qbar = 0
        self.ebar = 1
        self.cols = ['Periods', 'Output Gap', 'GDP', 'Inflation', 'Lending real i.r.', 'Lending nom i.r.', 'Real exchange rate', 
                    'q']

    def DemandShock(self, size, temporary=True):
        self.size = size
        self.multiplier = (0.01 * self.size) + 1
        df = pd.DataFrame(columns=self.cols)

        period = 1
        while period < 5:
            periodseries = pd.Series(dtype=np.float64)
            periodseries['Periods'] = period
            periodseries['Output Gap'] = 0.0
            periodseries['GDP'] = self.ye
            periodseries['Inflation'] = self.piT
            periodseries['Lending real i.r.'] = self.rstar
            periodseries['Lending nom i.r.'] = self.rstar - self.piT
            periodseries['Real exchange rate'] = self.ebar
            periodseries['q'] = self.qbar

            df.loc[period] = periodseries
            period += 1
        while period < 6:
            #periodseries = pd.Series(dtype=np.float64)
            periodseries['Periods'] = period
            #temporary demand shock
            periodseries['GDP'] = self.ye * self.multiplier
            periodseries['Output Gap'] = self.size
            inflation = self.piT + self.size
            periodseries['Inflation'] = inflation
            #cb response, finds PC where inflation = equilibrium output
            #then find that pc intersect with MR and that output is optimal bargaining gap
            #piE = df.loc[period - 1]['Inflation']
            cbresponsey = FindOptimumY(inflation, piT=self.piT, alpha=self.alpha)
            cbresponser = FindResponse(cbresponsey, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            periodseries['Lending real i.r.'] = cbresponser
            periodseries['Lending nom i.r.'] = cbresponser - inflation
            #newq = FindQ(cbresponser)
            periodseries['Real exchange rate'] = np.NaN
            periodseries['q'] = np.NaN

            df.loc[period] = periodseries
            period += 1
        
        while period <= self.periods:
            periodseries['Periods'] = period
            #beginning of recovery
            output = cbresponsey
            periodseries['GDP'] = output
            periodseries['Output Gap'] = output - self.ye
            inflation = InflationfromY(output, alpha=self.alpha, beta=self.beta, piT=self.piT)
            periodseries['Inflation'] = inflation
            #cb response, finds PC where inflation = equilibrium output
            #then find that pc intersect with MR and that output is optimal bargaining gap
            #piE = df.loc[period - 1]['Inflation']
            cbresponsey = FindOptimumY(inflation, piT=self.piT, alpha=self.alpha)
            cbresponser = FindResponse(cbresponsey, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            periodseries['Lending real i.r.'] = cbresponser
            periodseries['Lending nom i.r.'] = cbresponser - inflation
            #newq = FindQ(cbresponser)
            periodseries['Real exchange rate'] = np.NaN
            periodseries['q'] = np.NaN

            df.loc[period] = periodseries
            period += 1
        
        ##for exchange rates
        if temporary:
            ratesdiffsum = 0
            for x in df['Lending real i.r.'][5:]:
                x -= self.rstar
                ratesdiffsum += x
            ratesdiffsum *= 0.001
            if self.size > 0:
                ratesdiffsum += 0.03
                ratesdiffsum *= -1
            else:
                ratesdiffsum -= 0.03
                ratesdiffsum *= -1
            #print(ratesdiffsum)
            shockq = 10 ** (ratesdiffsum)
            #print(shockq)
            df.loc[5]['Real exchange rate'] = shockq
            df.loc[5]['q'] = ratesdiffsum

            x = 5
            while x <= self.periods - 1:
                ratediff = 0.01 * (df.loc[x]['Lending real i.r.'] - self.rstar)
                qE = self.qbar - ratediff
                df.loc[x+1]['Real exchange rate'] = 10 ** qE
                df.loc[x+1]['q'] = qE
                x+=1
        else:
            newqbar = NewQBarDemand(size, a=self.a, b=self.b, rstar=self.rstar, qbar=self.qbar)
            ratesdiffsum = 0
            for x in df['Lending real i.r.'][5:]:
                x -= self.rstar
                ratesdiffsum += x
            ratesdiffsum *= 0.001
            if self.size > 0:
                ratesdiffsum += 0.03
                ratesdiffsum *= -1
            else:
                ratesdiffsum -= 0.03
                ratesdiffsum *= -1

            
            #print(ratesdiffsum)
            shockq = 10 ** (newqbar + ratesdiffsum)
            #print(shockq)
            df.loc[5]['Real exchange rate'] = shockq
            df.loc[5]['q'] = (newqbar + ratesdiffsum)

            x = 5
            while x <= self.periods - 1:
                ratediff = 0.01 * (df.loc[x]['Lending real i.r.'] - self.rstar)
                qE = newqbar - ratediff
                df.loc[x+1]['Real exchange rate'] = 10 ** qE
                df.loc[x+1]['q'] = qE
                x+=1
        
        
        return df.round(4)

    def SupplyShock(self, size, temporary=True):
        self.size = size
        self.multiplier = (0.01 * self.size) + 1
        self.newye = self.ye * self.multiplier

        df = pd.DataFrame(columns=self.cols)

        period = 1
        while period < 5:
            periodseries = pd.Series(dtype=np.float64)
            periodseries['Periods'] = period
            periodseries['Output Gap'] = 0.0
            periodseries['GDP'] = self.ye
            periodseries['Inflation'] = self.piT
            periodseries['Lending real i.r.'] = self.rstar
            periodseries['Lending nom i.r.'] = self.rstar - self.piT
            periodseries['Real exchange rate'] = self.ebar
            periodseries['q'] = self.qbar

            df.loc[period] = periodseries
            period += 1
        
        while period < 6:
            #periodseries = pd.Series(dtype=np.float64)
            periodseries['Periods'] = period
            #permanent supply shock changes ye, not y
            periodseries['GDP'] = self.ye
            outputgap = ((self.ye - self.newye) / self.ye) * 100
            periodseries['Output Gap'] = outputgap
            inflation = self.piT + outputgap
            periodseries['Inflation'] = inflation
            #cb response, finds PC where inflation = equilibrium output
            #then find that pc intersect with MR and that output is optimal bargaining gap
            #piE = df.loc[period - 1]['Inflation']
            if temporary:
                cbresponsey = FindOptimumY(inflation, piT=self.piT, alpha=self.alpha)
                cbresponser = FindResponse(cbresponsey, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            else:
                cbresponsey = FindOptimumY(inflation, ye=self.newye, piT=self.piT, alpha=self.alpha)
                cbresponser = FindResponse(cbresponsey, ye=self.newye, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            periodseries['Lending real i.r.'] = cbresponser
            periodseries['Lending nom i.r.'] = cbresponser - inflation
            #newq = FindQ(cbresponser)
            periodseries['Real exchange rate'] = np.NaN
            periodseries['q'] = np.NaN

            df.loc[period] = periodseries
            period += 1

        while period <= self.periods:
            periodseries['Periods'] = period
            #beginning of recovery
            output = cbresponsey
            periodseries['GDP'] = output
            periodseries['Output Gap'] = output - self.ye
            if temporary:
                inflation = InflationfromY(output, alpha=self.alpha, beta=self.beta, piT=self.piT)
            else:
                inflation = InflationfromY(output, ye=self.newye, alpha=self.alpha, beta=self.beta, piT=self.piT)
            periodseries['Inflation'] = inflation
            #cb response, finds PC where inflation = equilibrium output
            #then find that pc intersect with MR and that output is optimal bargaining gap
            #piE = df.loc[period - 1]['Inflation']
            if temporary:
                cbresponsey = FindOptimumY(inflation, piT=self.piT, alpha=self.alpha)
                cbresponser = FindResponse(cbresponsey, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            else:
                cbresponsey = FindOptimumY(inflation, ye=self.newye, piT=self.piT, alpha=self.alpha)
                cbresponser = FindResponse(cbresponsey, ye=self.newye, a=self.a, b=self.b, alpha=self.alpha, beta=self.beta, rstar=self.rstar)
            periodseries['Lending real i.r.'] = cbresponser
            periodseries['Lending nom i.r.'] = cbresponser - inflation
            #newq = FindQ(cbresponser)
            periodseries['Real exchange rate'] = np.NaN
            periodseries['q'] = np.NaN

            df.loc[period] = periodseries
            period += 1

        ##for exchange rates
        if temporary: 
            ratesdiffsum = 0
            for x in df['Lending real i.r.'][5:]:
                x -= self.rstar
                ratesdiffsum += x
            ratesdiffsum *= 0.001
            if self.size < 0:
                ratesdiffsum += 0.03
                ratesdiffsum *= -1
            else:
                ratesdiffsum -= 0.03
                ratesdiffsum *= -1
            #print(ratesdiffsum)
            shockq = 10 ** (ratesdiffsum)
            #print(shockq)
            df.loc[5]['Real exchange rate'] = shockq
            df.loc[5]['q'] = ratesdiffsum

            x = 5
            while x <= self.periods - 1:
                ratediff = 0.01 * (df.loc[x]['Lending real i.r.'] - self.rstar)
                qE = self.qbar - ratediff
                df.loc[x+1]['Real exchange rate'] = 10 ** qE
                df.loc[x+1]['q'] = qE
                x+=1
        else:
            newqbar = NewQBarSupply(size, a=self.a, b=self.b, rstar=self.rstar, qbar=self.qbar)
            ratesdiffsum = 0
            for x in df['Lending real i.r.'][5:]:
                x -= self.rstar
                ratesdiffsum += x
            ratesdiffsum *= 0.001
            if self.size < 0:
                ratesdiffsum += 0.03
                ratesdiffsum *= -1
            else:
                ratesdiffsum -= 0.03
                ratesdiffsum *= -1

            
            #print(ratesdiffsum)
            shockq = 10 ** (newqbar + ratesdiffsum)
            #print(shockq)
            df.loc[5]['Real exchange rate'] = shockq
            df.loc[5]['q'] = newqbar + ratesdiffsum

            x = 5
            while x <= self.periods - 1:
                ratediff = 0.01 * (df.loc[x]['Lending real i.r.'] - self.rstar)
                qE = newqbar - ratediff
                df.loc[x+1]['Real exchange rate'] = 10 ** qE
                df.loc[x+1]['q'] = qE
                x+=1
        
        return df.round(4)


#temp inflation = negative temp supply, so use temp supply for it
#sim = Simulator()
#df = sim.SupplyShock(-3, temporary=True)
#print(df)
