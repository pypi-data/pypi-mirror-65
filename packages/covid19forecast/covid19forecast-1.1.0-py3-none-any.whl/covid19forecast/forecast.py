import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
import os
def confirmed_forecast(country_confirmed,next_periods,dir_name,csv_name,country):
	ObservationDate_x_ticks = []
	ObservationDate_confirmed=[]
	for index, row in country_confirmed.iterrows():
		ObservationDate_x_ticks.append(row['ObservationDate'])
		ObservationDate_confirmed.append(row['Confirmed'])
		ObservationDate_confirmed_prophet =country_confirmed[['ObservationDate', 'Confirmed']]
		ObservationDate_confirmed_prophet.columns = ['ds', 'y']
	model_confirmed = Prophet(interval_width=0.99)
	model_confirmed.fit(ObservationDate_confirmed_prophet)
	future_confirmed = model_confirmed.make_future_dataframe(periods=next_periods)
	forecast_confirmed = model_confirmed.predict(future_confirmed)
	model_confirmed.plot(forecast_confirmed)
	model_confirmed.plot_components(forecast_confirmed)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	forecast_confirmed_yhat = []
	forecast_confirmed_yhat_u = []
	forecast_confirmed_yhat_l = []
	for index, row in forecast_confirmed.iterrows():
		 forecast_confirmed_yhat.append(row['yhat'])
		 forecast_confirmed_yhat_l.append(row['yhat_lower'])
		 forecast_confirmed_yhat_u.append(row['yhat_upper'])
	plt.figure(figsize=(23,10))
	plt.xlabel('Days')
	plt.ylabel('Confirmed Case')
	plt.plot(forecast_confirmed_yhat, label='Prediction', color='blue')
	plt.plot(forecast_confirmed_yhat_l, label='Prediction lower', color='red')
	plt.plot(forecast_confirmed_yhat_u, label='Predicition upper', color='green')
	plt.title("Forecast of Confirmed Case ")
	plt.legend()
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_forecast_confirmed'+'.png')
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_forecasting_confirmed=pd.DataFrame(forecast_confirmed,columns=['ds','yhat','yhat_lower','yhat_upper'])
	country_forecasting_confirmed.to_csv(dir_name+'/forecast_confirmed_'+csv_name)
	return forecast_confirmed  
def deaths_forecast(country_death,next_periods,dir_name,csv_name,country):
	ObservationDate_x_ticks = []
	ObservationDate_country_death=[]
	for index, row in country_death.iterrows():
		ObservationDate_x_ticks.append(row['ObservationDate'])
		ObservationDate_country_death.append(row['Deaths'])
		ObservationDate_country_death_prophet =country_death[['ObservationDate', 'Deaths']]
		ObservationDate_country_death_prophet.columns = ['ds', 'y']
	model_country_death = Prophet(interval_width=0.99)
	model_country_death.fit(ObservationDate_country_death_prophet)
	future_country_death = model_country_death.make_future_dataframe(periods=next_periods)
	forecast_country_death = model_country_death.predict(future_country_death)
	model_country_death.plot(forecast_country_death)
	model_country_death.plot_components(forecast_country_death)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	forecast_country_death_yhat = []
	forecast_country_death_yhat_u = []
	forecast_country_death_yhat_l = []
	for index, row in forecast_country_death.iterrows():
		 forecast_country_death_yhat.append(row['yhat'])
		 forecast_country_death_yhat_l.append(row['yhat_lower'])
		 forecast_country_death_yhat_u.append(row['yhat_upper'])
	plt.figure(figsize=(23,10))
	plt.xlabel('Days')
	plt.ylabel('Deaths Case')
	plt.plot(forecast_country_death_yhat, label='Prediction', color='blue')
	plt.plot(forecast_country_death_yhat_l, label='Prediction lower', color='red')
	plt.plot(forecast_country_death_yhat_u, label='Predicition upper', color='green')
	plt.title("Forecast of Deaths Case ")
	plt.legend()
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_forecast_deaths'+'.png')
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_forecasting_country_death=pd.DataFrame(forecast_country_death,columns=['ds','yhat','yhat_lower','yhat_upper'])
	country_forecasting_country_death.to_csv(dir_name+'/forecast_deaths_'+csv_name)
	return forecast_country_death  
def recoverd_forecast(country_recoverd,next_periods,dir_name,csv_name,country):
	ObservationDate_x_ticks = []
	ObservationDate_country_recoverd=[]
	for index, row in country_recoverd.iterrows():
		ObservationDate_x_ticks.append(row['ObservationDate'])
		ObservationDate_country_recoverd.append(row['Recovered'])
		ObservationDate_country_recoverd_prophet =country_recoverd[['ObservationDate', 'Recovered']]
		ObservationDate_country_recoverd_prophet.columns = ['ds', 'y']
	model_country_recoverd = Prophet(interval_width=0.99)
	model_country_recoverd.fit(ObservationDate_country_recoverd_prophet)
	future_country_recoverd = model_country_recoverd.make_future_dataframe(periods=next_periods)
	forecast_country_recoverd = model_country_recoverd.predict(future_country_recoverd)
	model_country_recoverd.plot(forecast_country_recoverd)
	model_country_recoverd.plot_components(forecast_country_recoverd)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	forecast_country_recoverd_yhat = []
	forecast_country_recoverd_yhat_u = []
	forecast_country_recoverd_yhat_l = []
	for index, row in forecast_country_recoverd.iterrows():
		 forecast_country_recoverd_yhat.append(row['yhat'])
		 forecast_country_recoverd_yhat_l.append(row['yhat_lower'])
		 forecast_country_recoverd_yhat_u.append(row['yhat_upper'])
	plt.figure(figsize=(23,10))
	plt.xlabel('Days')
	plt.ylabel('Recovered Case')
	plt.plot(forecast_country_recoverd_yhat, label='Prediction', color='blue')
	plt.plot(forecast_country_recoverd_yhat_l, label='Prediction lower', color='red')
	plt.plot(forecast_country_recoverd_yhat_u, label='Predicition upper', color='green')
	plt.title("Forecast of Recovered Case ")
	plt.legend()
	#plt.show()
	plt.savefig(dir_name+'/'+country+'_forecast_recoverd'+'.png')
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
		print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
	country_forecasting_country_recoverd=pd.DataFrame(forecast_country_recoverd,columns=['ds','yhat','yhat_lower','yhat_upper'])
	country_forecasting_country_recoverd.to_csv(dir_name+'/forecast_recoverd_'+csv_name)
	return forecast_country_recoverd  
