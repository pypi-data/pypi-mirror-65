import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
import os
def all_cases(country,path_csv,dir_name,out_csv): 
	df = pd.read_csv(path_csv,parse_dates=['Last Update'])
	country_data = df[df['Country/Region']==country]
	#idata = country_data.tail(22)
	#idata.head()
	country_all_cases = country_data.groupby(["ObservationDate"])[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_cases=pd.DataFrame(country_all_cases ,columns=['ObservationDate','Confirmed','Deaths','Recovered'])
	country_cases.to_csv(dir_name+'/'+'all_cases_'+out_csv)
	plt.figure(figsize=(23,10))
	plt.bar(country_cases.ObservationDate, country_cases.Confirmed,label="Confirmed Case")
	plt.bar(country_cases.ObservationDate, country_cases.Deaths,label="Deaths Case")
	plt.bar(country_cases.ObservationDate, country_cases.Recovered,label="Recovered Case")

	plt.xlabel('Date')
	plt.ylabel("Count")
	plt.legend(frameon=True, fontsize=12)
	plt.title('All Cases',fontsize = 35)
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_all_cases'+'.png')
	return(country_cases)
def confirmed_case(country,path_csv,dir_name,out_csv): 
	df = pd.read_csv(path_csv,parse_dates=['Last Update'])
	country_data = df[df['Country/Region']==country]
	#idata = country_data.tail(22)
	#idata.head()
	country_confirmed = country_data.groupby(["ObservationDate"])[['Confirmed']].sum().reset_index()
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_confirmed_case=pd.DataFrame(country_confirmed ,columns=['ObservationDate','Confirmed'])
	country_confirmed_case.to_csv(dir_name+'/'+'confirmed_'+out_csv)
	plt.figure(figsize=(23,10))
	plt.bar(country_confirmed.ObservationDate, country_confirmed.Confirmed,label="Confirmed Case")
	plt.xlabel('Date')
	plt.ylabel("Count")
	plt.legend(frameon=True, fontsize=12)
	plt.title('Confirmed Case',fontsize = 35)
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_confirmed'+'.png')
	return(country_confirmed_case)
def deaths_case(country,path_csv,dir_name,out_csv): 
	df = pd.read_csv(path_csv,parse_dates=['Last Update'])
	country_data = df[df['Country/Region']==country]
	#idata = country_data.tail(22)
	#idata.head()
	country_death = country_data.groupby(["ObservationDate"])[['Deaths']].sum().reset_index()
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_death_case=pd.DataFrame(country_death ,columns=['ObservationDate','Deaths'])
	country_death_case.to_csv(dir_name+'/'+'death_'+out_csv)
	plt.figure(figsize=(23,10))
	plt.bar(country_death.ObservationDate, country_death.Deaths,label="Deaths Case")
	plt.xlabel('Date')
	plt.ylabel("Count")
	plt.legend(frameon=True, fontsize=12)
	plt.title('Deaths Case',fontsize = 35)
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_deaths'+'.png')
	return(country_death_case)
def recoverd_case(country,path_csv,dir_name,out_csv): 
	df = pd.read_csv(path_csv,parse_dates=['Last Update'])
	country_data = df[df['Country/Region']==country]
	#idata = country_data.tail(22)
	#idata.head()
	country_recoverd = country_data.groupby(["ObservationDate"])[['Recovered']].sum().reset_index()
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_recoverd_case=pd.DataFrame(country_recoverd ,columns=['ObservationDate','Recovered'])
	country_recoverd_case.to_csv(dir_name+'/'+'recoverd_'+out_csv)
	plt.figure(figsize=(23,10))
	plt.bar(country_recoverd.ObservationDate, country_recoverd.Recovered,label="Recovered Cases")
	plt.xlabel('Date')
	plt.ylabel("Count")
	plt.legend(frameon=True, fontsize=12)
	plt.title('Recovered Case',fontsize = 35)
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_recoverd'+'.png')
	return(country_recoverd_case)