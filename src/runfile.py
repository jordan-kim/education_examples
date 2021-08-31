from src import process,IVfitting, Measured_Spectra, Processed_spectra, Ref_fitting, Rsqu
import glob, time, os
from tqdm import tqdm
from src import datalocation1 as dl


def run(file_path, folder, shape, wafer, save, show, csv, jupyter,version):
    xml=[]
    for filename in glob.glob(file_path, recursive= True):
        xml.append(filename)


    start = time.time()

    custom_want = folder

    custom_want = custom_want.split(',')
    if ('D07' or 'D08' or 'D23' or 'D24') not in custom_want:
        print('분석하실 Folder를 다시 입력하여 주세요')


    if 'D07' in custom_want:
        d = 1
    else:
        d = 0
    if 'D08' in custom_want:
        e = 1
    else:
        e = 0
    if 'D23' in custom_want:
        f = 1
    else:
        f = 0
    if 'D24' in custom_want:
        g = 1
    else:
        g = 0

    if d == 1 and e == 0 and f == 0 and g == 0 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
    elif e == 1 and d == 0 and f == 0 and g == 0 :
        file_path0 = dl.data(file_path, 'D08')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
    elif f == 1 and d == 0 and e == 0 and g == 0 :
        file_path0 = dl.data(file_path, 'D23')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
    elif g == 1 and f == 0 and d == 0 and e == 0 :
        file_path0 = dl.data(file_path, 'D24')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)

    elif d == 1 and e == 1 and f == 0 and g == 0 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D08')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
    elif d == 1 and e == 0 and f == 1 and g == 0 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D23')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
    elif d == 1 and e == 0 and f == 0 and g == 1 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
    elif d == 0 and e == 1 and f == 1 and g == 0 :
        file_path0 = dl.data(file_path, 'D08')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D23')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
    elif d == 0 and e == 1 and f == 0 and g == 1 :
        file_path0 = dl.data(file_path, 'D08')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
    elif d == 0 and e == 0 and f == 1 and g == 1 :
        file_path0 = dl.data(file_path, 'D23')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)

    elif d == 1 and e == 1 and f == 1 and g == 0 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D08')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
        file_path2 = dl.data(file_path, 'D23')
        for filename in glob.glob(file_path2, recursive=True):
            xml.append(filename)
    elif d == 1 and e == 1 and f == 0 and g == 1 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D08')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
        file_path2 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path2, recursive=True):
            xml.append(filename)
    elif d == 1 and e == 0 and f == 1 and g == 1 :
        file_path0 = dl.data(file_path, 'D07')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D23')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
        file_path2 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path2, recursive=True):
            xml.append(filename)
    elif d == 0 and e == 1 and f == 1 and g == 1 :
        file_path0 = dl.data(file_path, 'D08')
        xml = []
        for filename in glob.glob(file_path0, recursive=True):
            xml.append(filename)
        file_path1 = dl.data(file_path, 'D23')
        for filename in glob.glob(file_path1, recursive=True):
            xml.append(filename)
        file_path2 = dl.data(file_path, 'D24')
        for filename in glob.glob(file_path2, recursive=True):
            xml.append(filename)
    else:
            xml = []
            for filename in glob.glob(file_path, recursive=True):
                xml.append(filename)

    xml1 = []
    wafer = wafer.split(' ')
    for i in xml:
        for x in wafer:
            if x in i:
                xml1.append(i)
            elif x == 'ALL':
                xml1.append(i)

    custom_f = shape
    custom_f = custom_f.split(',')

    if ('All_fig' or 'Transmission' or 'IV' or 'fitting' or 'spectra') not in custom_f:
        print('Figure Shape를 다시 입력하여 주세요')


    if 'All_fig' in custom_f: # All
        aa = 1
    else:
        aa = 0
    if 'Transmission' in custom_f: # Transmission
        bb = 2
    else:
        bb = 0
    if 'IV' in custom_f: # IV raw dat
        cc = 3
    else:
        cc = 0
    if 'fitting' in custom_f: # Processed and fitting
        dd = 4
    else:
        dd = 0
    if 'spectra' in custom_f: # Processed spectra
        ee = 5
    else:
        ee = 0
    custom_W = show
    custom_a = save
    custom_c = csv

    # show figure 옵션
    if custom_W == 'T':
        custom_w = 1
    else:
        custom_w = 0
    # save figure 옵션
    if custom_a == 'T':
        custom_a = 1
    else:
        custom_a = 0

    if custom_c =='T':
        custom_c = 1
    else:
        custom_c = 0


    xml_tqdm = tqdm(xml1)
    for i in xml_tqdm:
        # fitting 실행
        filename = i.split('\\')[-1][:-4]
        xml_tqdm.set_description(f'Processing {filename}')
        if aa == 1:
            process.fitting(i, custom_a, custom_w, version)
        elif bb == 2:
            Measured_Spectra.Measured(i, custom_a, custom_w, version)
        elif cc == 3:
            if Rsqu.Rsqu(i) < 0.95:
                print('데이터를 다시 한번 확인해주세요.')
            IVfitting.IVfitting(i, custom_a, custom_w, version)
        elif dd == 4:
            Ref_fitting.Ref_fitting(i, custom_a, custom_w, version)
        else:
            Processed_spectra.Pro_spe(i, custom_a, custom_w, version)
        process.csv_mod(i, version, custom_c)

    if int(xml1.index(i)) + 1 == len(xml1):
        print("All files are complete. Thank you for your efforts")

    print("Run Time :" + str(round(time.time() - start, 1)) + "seconds")

    jupyter = jupyter
    if jupyter == 'T':
        os.system("jupyter notebook")