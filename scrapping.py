import requests

url = 'https://www.ess-geneve.ch/accueil-ete/'

response = requests.get(url)
code = response.status_code
print(code)
