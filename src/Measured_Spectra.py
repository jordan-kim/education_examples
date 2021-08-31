from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action='ignore')
import os
def Measured(filename,custom_a,custom_w,version):

    fp = open(filename, "r")

    soup = BeautifulSoup(fp,"html.parser")


    # label
    wavelengthsweep = soup.findAll('wavelengthsweep')
    label = []
    for i in range(0, 7):
        label.append(wavelengthsweep[i]['dcbias'])  # append가 list에 뭔가를 추가

    # Measured raw dat

    for i in range(0, 7):
        wavelength = soup.findAll('wavelengthsweep')[i]('l')[0].string
        WL = wavelength.split(',')
        wl = list(map(float, WL))

        IL = soup.findAll('wavelengthsweep')[i]('il')[0].string
        Il = IL.split(',')
        il = list(map(float, Il))
        if i < 6:
            plt.scatter(wl, il, s = 1, alpha=0.3, label=label[i] + 'V')
        else:
            plt.scatter(wl, il, s = 1 ,alpha=0.3)

    plt.title("Transmission spectra - as measured", fontsize=15)
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Measured transmission [dB]")
    plt.legend(loc='lower center', ncol=3)

    fname = filename.split('\\')[-1][:-4]
    plt.suptitle(fname)
    fig = plt.gcf()
    fig.set_size_inches((27, 15), forward=False)

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