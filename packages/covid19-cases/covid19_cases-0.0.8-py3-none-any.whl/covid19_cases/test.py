import urllib.request
from bs4 import BeautifulSoup as bf
import time
import corona19
country='egypt'
iraq1=corona19.confirmed_people(country)
iraq2=corona19.deaths_people(country)
iraq3=corona19.recoverd_people(country)
print(iraq1)
print(iraq2)
print(iraq3)

