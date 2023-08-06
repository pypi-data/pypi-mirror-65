# Covid19 Cases Tracking For Every Country in Real Time 

## about

A small package of Python to access and track the number of cases of confirmed and deaths and  recovered people
from the Coronavirus for any country 

# Installation

```
pip install covid19-cases
or in colab google cloud
!pip install covid19-cases
```

## Usage

```
from covid19_cases import corona19
country_name='any_country' #name of country 
```

```
# to get confirmed count for country in real time
confirmed_count=corona19.confirmed_people(country_name)
#to get deaths count for country in real time 
deaths_count=corona19.deaths_people(country_name)
#to get recoverd count in real time 
recoverd_count=corona19.recoverd_people(country_name)
```

## Checking

To verify the retrieved data within this library
go to worldmeters web site for checking for any coutry

https://www.worldometers.info/coronavirus



 

