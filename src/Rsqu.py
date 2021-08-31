from bs4 import BeautifulSoup
import numpy as np
from numpy import exp
import statsmodels.api as sm



def poly(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    # r-squared
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
    ssreg = np.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
    results = ssreg / sstot
    return results

def Rsqu(filename):
    fp = open(filename, "r")
    soup = BeautifulSoup(fp, "html.parser")
    voltage = soup.findAll('voltage')[0].string.split(',')
    current = soup.findAll('current')[0].string.split(',')
    x = list(map(float, voltage))
    y = list(map(float, current))
    y = np.abs(y)
    C = np.array(y[:10])
    V = np.array(x[:10])
    fit1 = np.polyfit(V, C, 11)
    fit1 = np.poly1d(fit1)
    # I = a(exp(bV-1)+alpha
    def IV_fit(x, a, b):
        return (a * (exp(b * x) - 1) + fit1(x))
    initial_list = []
    for i in x:
        x_value = IV_fit(i, 10e-16, 1 / 0.026)
        initial_list.append(x_value)
    initial = sm.add_constant(np.abs(y))
    result1 = sm.OLS(initial_list, initial).fit()
    Rsq = result1.rsquared
    return Rsq

