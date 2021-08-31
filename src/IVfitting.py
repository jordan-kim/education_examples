from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model
from numpy import exp
import statsmodels.api as sm
import warnings
warnings.filterwarnings(action='ignore')
import os
import time

def IVfitting(filename,custom_a,custom_w, version):

    fp = open(filename, "r")

    soup = BeautifulSoup(fp,"html.parser")

    voltage = soup.findAll('voltage')[0].string.split(',')
    current = soup.findAll('current')[0].string.split(',')

    x = list(map(float, voltage))
    y = list(map(float, current))
    y = np.abs(y)

    # 2번째 그래프

    plt.title("IV raw dat & fitted dat", fontsize=15)
    plt.xlabel("Voltage [V]")
    plt.ylabel("Current [A]")

    plt.yscale("log")
    plt.plot(x, np.abs(y), 'ko')

    C = np.array(y[:10])
    V = np.array(x[:10])
    fit1 = np.polyfit(V, C, 11)
    fit1 = np.poly1d(fit1)

    # I = a(exp(bV-1)+alpha
    def IV_fit(x, a, b):
        return (a * (exp(x/b) - 1) + fit1(x))

    model = Model(IV_fit)
    result = model.fit(y, x=x, a=2.28 * 10 ** -15, b=0.0351)

    initial_list = []
    for i in x:
        x_value = IV_fit(i, 2.28 * 10 ** -15, 0.0351)
        initial_list.append(x_value)

    initial = sm.add_constant(np.abs(y))
    result1 = sm.OLS(initial_list, initial).fit()

    IVdic = {y: x for x, y in zip(result.best_fit, x)}
    plt.text(1.0, IVdic[1.0], IVdic[1.0], fontsize=8, horizontalalignment='right')
    plt.text(-1.0, IVdic[-1.0], IVdic[-1.0], fontsize=8)
    plt.plot(x, result.best_fit, 'r-', label='{} {}'.format('$R^{2}$ =', result1.rsquared))
    plt.legend(loc='center left')

    fname = filename.split('\\')[-1][:-4]
    plt.suptitle(fname)
    fig = plt.gcf()
    fig.set_size_inches((27,15), forward=False)

    if custom_a == 1:
        if not os.path.exists('.\\res\\figure%s' % version):
            os.makedirs('.\\res\\figure%s' % version)
        if not os.path.exists('.\\res\\figure%s\\%s' % (version, filename.split('\\')[2])):
            os.makedirs('.\\res\\figure%s\\%s' % (version, filename.split('\\')[2]))
        if not os.path.exists('.\\res\\figure%s\\%s\\%s' % (version, filename.split('\\')[2], filename.split('\\')[3])):
            os.makedirs('.\\res\\figure%s\\%s\\%s' % (version, filename.split('\\')[2], filename.split('\\')[3]))
        if not os.path.exists(
                '.\\res\\figure%s\\%s\\%s\\%s' % (version, filename.split('\\')[2], filename.split('\\')[3],
                                                  filename.split('\\')[4])):
            os.makedirs('.\\res\\figure%s\\%s\\%s\\%s' % (version, filename.split('\\')[2], filename.split('\\')[3],
                                                          filename.split('\\')[4]))
        plt.savefig('.\\res\\figure%s\\%s\\%s\\%s\\%s.png' % (version, filename.split('\\')[2], filename.split('\\')[3],
                                                              filename.split('\\')[4], fname))
        if custom_w == 0:
            plt.show(block=False)
            plt.close()
    # show figure 옵션

    if custom_w == 1:
        plt.show()