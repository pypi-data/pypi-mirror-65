import urllib.request
from bs4 import BeautifulSoup as bf
import time
import covid19 as covid




i1=covid.confirmed_people()
i2=covid.deaths_people()
i3=covid.recoverd_people()
i4=covid.confirmed_people_regions('SoussMassa')
print(i1)
print(i2)
print(i3)
print(i4)

covid.hist_cases()

covid.plot_cases()


