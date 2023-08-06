# Covid19  Forecasting For all Cases in future using fbprophet model

## about

Python Package to get Covid19  Forecasting For all Cases  in future



# Installation

```
pip install covid19forecast
or in colab google cloud
!pip install covid19forecast
```

## Usage for get first cases (confirmed,recoverd,deaths for any countery)

```
from covid19forecast import cases 
```
```
# country name
country='Iraq'
#path for covide19 dataset   
path_csv='covid_19_data.csv'
#name of  folder  
dir_name='Iraq'
# name of out result for all cases in new dataset 
out_csv='iraq.csv'
# what days number to forecasting for any case 
next_periods=10
# what name of dataset for all forecasting for any case
csv_name='iraq.csv'

```

```
# to get all cases for country 
all=cases.all_cases(country,path_csv,dir_name,out_csv)

# to get confirmed cases for country 
confirmed=cases.confirmed_case(country,path_csv,dir_name,out_csv)
#to get deaths  cases for country 
deaths=cases.deaths_case(country,path_csv,dir_name,out_csv)

#to get recoverd cases for country 
recoverd=cases.recoverd_case(country,path_csv,dir_name,out_csv)


```

## Usage for get Forcasting for all  cases (confirmed,recoverd,deaths for any countery)

```
from covid19forecast import forecast 
```
```
# to get forecasting for country confirmed case
forecast.confirmed_forecast(confirmed,next_periods,dir_name,csv_name,country)
# to get forecasting for country deaths case
forecast.deaths_forecast(deaths,next_periods,dir_name,csv_name,country)
# to get forecasting for country recoverd case
forecast.recoverd_forecast(recoverd,next_periods,dir_name,csv_name,country)
```
## Checking

To verify the retrieved data within this library
go to web site to get download new covid19 dataset

https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset

## Tutorial 
u can see tutorial in colab 

https://colab.research.google.com/drive/12TnzM0E-oZgsrwlaQ5vYCdhsym6UDNUa


 

