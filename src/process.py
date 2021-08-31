from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil.parser import parse
from lmfit import Model
from numpy import exp
import statsmodels.api as sm
import os
import warnings

warnings.filterwarnings(action='ignore')


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


def fitting(filename, custom_a, custom_w,version):
    fp = open(filename, "r")

    soup = BeautifulSoup(fp, "html.parser")

    # label
    wavelengthsweep = soup.findAll('wavelengthsweep')
    label = []
    for i in range(0, 7):
        label.append(wavelengthsweep[i]['dcbias'])  # append가 list에 뭔가를 추가

    voltage = soup.findAll('voltage')[0].string.split(',')
    current = soup.findAll('current')[0].string.split(',')

    grid = (12, 12)

    x = list(map(float, voltage))
    y = list(map(float, current))
    y = np.abs(y)

    # 2번째 그래프
    plt.rcParams['figure.figsize'] = [18, 15]
    plt.subplot2grid(grid, (7, 0), rowspan=5, colspan=5)

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
        return (a * (exp(x / b) - 1) + fit1(x))

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

    # 1번째 그래프
    plt.subplot2grid(grid, (0, 0), rowspan=5, colspan=5)

    for i in range(0, 7):
        wavelength = soup.findAll('wavelengthsweep')[i]('l')[0].string
        WL = wavelength.split(',')
        wl = list(map(float, WL))

        IL = soup.findAll('wavelengthsweep')[i]('il')[0].string
        Il = IL.split(',')
        il = list(map(float, Il))
        if i < 6:
            plt.scatter(wl, il, s=1, alpha=0.3, label=label[i] + 'V')
        else:
            plt.scatter(wl, il, s=1, alpha=0.3)

    plt.title("Transmission spectra - as measured", fontsize=15)
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Measured transmission [dB]")
    plt.legend(loc='lower center', ncol=3)

    refx = list(map(float, soup.findAll('wavelengthsweep')[6]('l')[0].string.split(',')))
    refy = list(map(float, soup.findAll('wavelengthsweep')[6]('il')[0].string.split(',')))

    # 3번째 그래프
    plt.subplot2grid(grid, (0, 7), rowspan=5, colspan=5)
    squared = []
    for i in range(1, 7):
        z = np.polyfit(refx, refy, i)
        f = np.poly1d(z)
        x_new = np.linspace(refx[0], refx[-1], 50)
        y_new = f(x_new)
        plt.plot(x_new, y_new, label=str(i) + 'th')
        p = poly(refx, refy, i)
        squared.append(p)

    # R-squared
    squ = 0.95
    a = 0
    for i in range(4, 6):
        if squared[i] > squ:
            squ = squared[i]
            a = i
        else:
            squ = squ

    plt.text(np.median(refx), refy[600], "%dth R-squ = %s" % (a + 1, squ), horizontalalignment='center', size=9,
             color='r')
    plt.legend(loc='lower center', ncol=3)
    plt.scatter(refx, refy, facecolor='none', edgecolor='r', s=1, alpha=0.5)
    plt.title('Transmission spectra - Processed and fitting')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Measured transmission [dB]')

    # 4번째 그래프
    plt.subplot2grid(grid, (7, 7), rowspan=5, colspan=5)
    for i in range(0, 6):
        wavelength = soup.findAll('wavelengthsweep')[i]('l')[0].string
        WL = wavelength.split(',')
        wl = list(map(float, WL))

        IL = soup.findAll('wavelengthsweep')[i]('il')[0].string
        Il = IL.split(',')
        il = list(map(float, Il))

        x = wl
        y = il - f(wl)

        if i < 6:
            plt.scatter(x, y, s=1, alpha=0.3, label=label[i] + 'V')
    plt.legend(bbox_to_anchor=(0.25, 1.08, 0.5, 0.05), ncol=3, loc='lower center')

    plt.title("Transmission spectra except ref.dat", fontsize=15)
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Measured transmission [dB]")

    # filename 수정_수업시간
    fname = filename.split('\\')[-1][:-4]
    plt.suptitle(fname, fontsize = 27)
    fig = plt.gcf()
    fig.set_size_inches((27, 15), forward=False)

    # save figure 옵션

    if custom_a == 1:
        if not os.path.exists('.\\res\\figure%s'%version):
            os.makedirs('.\\res\\figure%s'%version)
        if not os.path.exists('.\\res\\figure%s\\%s'%(version,filename.split('\\')[2])):
            os.makedirs('.\\res\\figure%s\\%s'%(version, filename.split('\\')[2]))
        if not os.path.exists('.\\res\\figure%s\\%s\\%s'%(version,filename.split('\\')[2], filename.split('\\')[3])):
            os.makedirs('.\\res\\figure%s\\%s\\%s'%(version,filename.split('\\')[2], filename.split('\\')[3]))
        if not os.path.exists('.\\res\\figure%s\\%s\\%s\\%s'%(version, filename.split('\\')[2], filename.split('\\')[3],
                                                                  filename.split('\\')[4])):
            os.makedirs('.\\res\\figure%s\\%s\\%s\\%s'%(version,filename.split('\\')[2], filename.split('\\')[3],
                                                            filename.split('\\')[4]))
        plt.savefig('.\\res\\figure%s\\%s\\%s\\%s\\%s.png'%(version,filename.split('\\')[2], filename.split('\\')[3],
                                                                filename.split('\\')[4], fname))

    # show figure 옵션

    if custom_w == 1:
        plt.show()


#######################################################################################################################
#######################################################################################################################


def csv_mod(filename,version ,custom_csv):
    fp = open(filename, "r")
    soup = BeautifulSoup(fp, "html.parser")

    voltage = soup.findAll('voltage')[0].string.split(',')
    current = soup.findAll('current')[0].string.split(',')

    x = list(map(float, voltage))
    y = list(map(float, current))
    y = np.abs(y)

    # 2번째 그래프

    C = np.array(y[:10])
    V = np.array(x[:10])
    fit1 = np.polyfit(V, C, 11)
    fit1 = np.poly1d(fit1)

    # I = a(exp(bV-1)+alpha
    def IV_fit(x, a, b):
        return (a * (exp(b * x) - 1) + fit1(x))

    model = Model(IV_fit)
    result = model.fit(y, x=x, a=10e-16, b=1 / 0.026)

    initial_list = []
    for i in x:
        x_value = IV_fit(i, 10e-16, 1 / 0.026)
        initial_list.append(x_value)

    initial = sm.add_constant(np.abs(y))
    result1 = sm.OLS(initial_list, initial).fit()
    IVdic = {y: x for x, y in zip(result.best_fit, x)}
    refx = list(map(float, soup.findAll('l')[6].string.split(',')))
    refy = list(map(float, soup.findAll('il')[6].string.split(',')))

    Rsqref = poly(refx, refy, 6)

    Lot = soup.select('testsiteinfo')[0]['batch']
    Wafer = soup.select('testsiteinfo')[0]['wafer']
    Mask = soup.select('testsiteinfo')[0]['maskset']
    Column = soup.select('testsiteinfo')[0]['diecolumn']
    Row = soup.select('testsiteinfo')[0]['dierow']
    TestSite = soup.select('testsiteinfo')[0]['testsite']
    Name = soup.select("modulator")[0]['name']

    Date = soup.select('oiomeasurement')[0]['creationdate']
    Date = parse(Date).strftime("%Y%m%d_%H%M%S")

    error_flag_list = []
    error_description = []
    WL_list = []
    Rsq = result1.rsquared
    if Rsq < 0.95:
        error_flag_list.append(1)
        error_description.append('Rsq error')
    else:
        error_flag_list.append(0)
        error_description.append('No error')

    WL_analy = soup.findAll('designparameter')
    for k in range(0, len(WL_analy)):
        if WL_analy[k]['symbol'] == 'WL':
            WL_list.append(WL_analy[k].text)

    df = pd.DataFrame(columns=['Lot', 'Wafer', 'Mask', 'TestSite', 'Name', 'Date', 'Script ID',
                               'Script Version', 'Script Owner', 'Operator', 'Row', 'Column',
                               'ErrorFlag', 'Error description', 'Analysis Wavelength', 'Rsq of Ref.spectrum (Nth)',
                               'Max transmission of Ref. spec. (dB)', 'Rsq of IV', 'I at -1V [A]', 'I at 1V [A]'])

    df.loc[0] = [Lot, Wafer, Mask, TestSite, Name, Date, 'process LMZ', '0.1', 'A02',
                 'JoohanBae,Parkseoungmin,Jeonsuin', Row, Column,
                 error_flag_list[0],
                 error_description[0], WL_list[0], Rsqref, max(refy), Rsq, IVdic[-1.0], IVdic[1.0]]



    if custom_csv == 1:
        location = 'process_Result%s.csv'%version
        # if datetime.datetime.now().minute in os.path.basename('.\\res\\csv\\'):
        if not os.path.exists('.\\res\\csv\\%s'%location):
            try:
                os.makedirs('.\\res\\csv\\')
            except:
                FileExistsError
                pass
            df.to_csv('.\\res\\csv\\%s'%location, mode='w', index=False)
        else:
            df.to_csv('.\\res\\csv\\%s'%location, mode='a', index=False, header=False)






