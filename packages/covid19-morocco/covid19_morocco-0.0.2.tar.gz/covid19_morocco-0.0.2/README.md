# Covid19 Cases Tracking in Morocco in Real Time 

## about

A small package of Python to access and track the number of cases of confirmed and deaths and  recovered people
from the Coronavirus for Morocco

# Installation

```
pip install covid19_morocco
or in colab google cloud
!pip install covid19_morocco
```

## Usage

```
from covid19_morocco import covid19
country_name=Morocco #name of country 
```

```
# to get confirmed count for country in real time
confirmed_count=covid19.confirmed_people()
#to get deaths count for country in real time 
deaths_count=covid19.deaths_people()
#to get recoverd count in real time 
recoverd_count=covid19.recoverd_people()
# to get confirmed cases by regions (SoussMassa, CasaSettat, FesMeknes, MarrakechSafi,....)
confirmed_by_regions=covid19.confirmed_people_regions(regions)
#Plot cases 
covid19.plot_cases()
#Plot histogram
covid19.hist_cases()
```

## Checking

To verify the retrieved data within this library
go to worldmeters web site for checking for any coutry

https://www.worldometers.info/coronavirus

plot cases
https://raw.githubusercontent.com/aboullaite/Covid19-MA/master/stats/MA-times_series.csv





 

