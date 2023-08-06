import requests
from bs4 import BeautifulSoup

url = requests.get("https://pr-cy.ru/browser-details/")
html = BeautifulSoup(url.content, "html.parser")

def get_ip():
	ip = html.select(".ip")
	return ip[0].text

def get_city():
	city = html.select(".ip")
	return city[1].text

def get_country():
	country = html.select(".ip")
	return country[2].text

