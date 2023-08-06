import urllib.request
from bs4 import BeautifulSoup as bf
import time

state='Morocco'
def confirmed_people():
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	confirmed_people = tag[4].contents[0]
	return(confirmed_people)

def deaths_people():
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	death_people = tag[5].contents[0]
	return(death_people)

def recoverd_people():
	time.sleep(5)
	#url = 'https://www.google.com/search?q=python'
	url='https://www.worldometers.info/coronavirus/country/'+state+'/'
	# now, with the below headers, we defined ourselves as a simpleton who is
	# still using internet explorer.
	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	req = urllib.request.Request(url, headers = headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	soup = bf(respData,'html.parser')
	tag = soup("span")
	recovers_people = tag[6].contents[0]
	return(recovers_people)

def confirmed_people_regions(city):
    json_url ="https://moroccostats.herokuapp.com/stats/coronavirus/countries/morocco/regions?fbclid=IwAR3KpT3JArtFc83s14sOJsT99pIx8UFqfHWZgfN4oxAr6OLj05apXvdWmqY"
    import requests
    import json    
    # download the raw JSON
    raw = requests.get(json_url).text
    
    data = json.loads(raw)
    #print(data['SoussMassa'])
    return(data[city])
    
    if city=='BeniMellalKhnifra':
        return(data['BeniMellalKhnifra'])
    
    elif city=='DaraaTafilalet':
        return(data['Daraatafilalet'])
    
    elif city=='FesMeknes':
        return(data['Fsmeknes'])
    
    elif city=='LaayouneSakiaElHamra':
        return(data['LayouneSakiaElHamra'])
    
    elif city=='Oriental':
        return(data['Oriental'])
    
    elif city=='SoussMassa':
        return(data['SoussMassa'])
        
    elif city=='CasaSettat':
        return(data['CasaSettat'])
        
    elif city=='DakhlaOuedEdDahab':
        return(data['DakhlaOuedEdDahab'])
        
    elif city=='GuelmimOuedNoun':
        return(data['GuelmimOuedNoun'])
        
    elif city=='MarrakechSafi':
        return(data['MarrakechSafi'])
        
    elif city=='RabatSaleKenitra':
        return(data['RabatSalKenitra'])
        
    elif city=='TangerTetouanAlHoceima':
        return(data['TangerTetouanAlHoceima'])
    

def plot_cases():
    
    json_url ="https://raw.githubusercontent.com/aboullaite/Covid19-MA/master/stats/MA-times_series.csv"
    
    import pandas as pd
    df = pd.read_csv(json_url,index_col=0)
    
    df = df.rename(columns={'Dates / التواريخ': 'Dates', 'Cases / الحالات': 'Cases', 'Recovered / تعافى': 'Recovered', 'Deaths / الوفيات': 'Deaths'})
    df=df.drop(columns=['Recovered'])
    
    from matplotlib import pyplot
    
    df.plot(marker='o', figsize=(15,5))
    
    pyplot.xticks(rotation = 50)
    pyplot.xlabel("Dates")
    pyplot.show()

def hist_cases():
    json_url ="https://raw.githubusercontent.com/aboullaite/Covid19-MA/master/stats/MA-times_series.csv"

    import pandas as pd
    df = pd.read_csv(json_url,index_col=0)
    
    df = df.rename(columns={'Dates / التواريخ': 'Dates', 'Cases / الحالات': 'Cases', 'Recovered / تعافى': 'Recovered', 'Deaths / الوفيات': 'Deaths'})
    df=df.drop(columns=['Recovered'])
    
    from matplotlib import pyplot
    
    #df.plot(marker='o')
    df.plot(kind='bar', figsize=(15,5))
    pyplot.xticks(rotation = 50)
    pyplot.xlabel("Dates")
    pyplot.show()


    
    
    
    
    