from bs4 import BeautifulSoup
from dateutil.parser import parse


def Date(filename):
    fp = open(filename, "r")
    soup = BeautifulSoup(fp, "html.parser")
    Date = soup.select('oiomeasurement')[0]['creationdate']
    Date = parse(Date).strftime("%Y%m%d_%H시%M분%S초")
    print(filename.split('\\')[-1][:-4], '는', Date, '에 측정되었습니다.')