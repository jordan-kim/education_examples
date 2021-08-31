# a = '.\dat\P184640\**\*LMZ?.xml'
def data(dirpath,a):
    file_Path = dirpath[:dirpath.find('\\**')] +'\\'+ a + dirpath[dirpath.find('\\**'):]
    return file_Path
