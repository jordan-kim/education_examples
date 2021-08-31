from src import runfile as rs
from src import Time

# Data location
path = ('.\dat\HY202103\**\*LMZ?.xml')

# Analyze Folder
# 분석하실 폴더를 선택하여 주세요  (중복선택시 ',' 포함) [D07, D08, D23, D24]
folder = 'D07,D08'

# Figure shape
# 분석하실 그래프의 모양을 선택하여 주세요 (중복선택은 불가합니다!) [All_fig, Transmission, IV , fitting, spectra]
shape = 'All_fig'

# Column & Row
# 분석하실 그래프의 Column & Row를 선택하여 주세요 (중복선택시 ' ' 포함)
# ('ALL','(-1,-1)','(-1,-3)','(-1,3)','(-3,-3)','(-3,0)','(-3,2)','(-4,-1)','(0,-4)','(0,0)','(0,2)','(2,-1)','(2,-3)','(2,2)','(3,0)')
wafer = '(-1,-1) (-1,3)'

# Save figure('T/F')
save = 'T'

# Show figure('T/F')
show = 'T'

# Save CSV('T/F')
csv = 'T'

# Jupyter notebook (Documentation)
jupyter = 'T'


rs.run(path, folder, shape, wafer, save, show, csv, jupyter, Time.time())