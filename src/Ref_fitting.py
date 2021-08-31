from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings(action='ignore')
import os

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

def Ref_fitting(filename,custom_a,custom_w,version):

    fp = open(filename, "r")

    soup = BeautifulSoup(fp,"html.parser")



    refx = list(map(float, soup.findAll('wavelengthsweep')[6]('l')[0].string.split(',')))
    refy = list(map(float, soup.findAll('wavelengthsweep')[6]('il')[0].string.split(',')))

    # 3번째 그래프

    squared = []
    for i in range(1, 9):
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
    for i in range(5, 8):
        if squared[i] > squ:
            squ = squared[i]
            a = i
        else:
            squ = squ

    plt.text(np.median(refx), refy[600], "%dth R-squ = %s" % (a , squ), horizontalalignment='center', size=9, color='r')
    plt.legend(loc='lower center', ncol=3)
    plt.scatter(refx, refy, facecolor='none', edgecolor='r', s=1, alpha=0.5)
    plt.title('Transmission spectra - Processed and fitting')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Measured transmission [dB]')

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