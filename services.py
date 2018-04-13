from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import os
import time



global chrome_options
global chromedriver
global driver


def configure_headless():
	global chrome_options
	global chromedriver
	global driver

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=1920x1080")
	chrome_driver = os.getcwd() +"/chromedriver"

	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


def stackoverflow(question):
	configure_headless()
	global chrome_options
	global chromedriver
	global driver
	driver.get("https://stackoverflow.com/")

	search = driver.find_element_by_xpath("/html/body/header/div/form/input")
	search.send_keys(question)

	search_button = driver.find_element_by_xpath("/html/body/header/div/form/button")
	search_button.click()

	return driver.current_url
	
def display_answers(questions, answers):
	index = 0

	for index in range(0, len(questions)):
		print colored(questions[index].text.replace("  ",""), 'red')

		link = questions[index]
		for a in link.find_all('a'):
			if a.has_attr('href'):
				ans = a.attrs['href']
		print colored('http://stackoverflow.com'+ans, 'green')

		print colored(answers[index].text.replace("  ",""), 'blue')

def kill_browser():
	driver.close()
	driver.quit()

def get_answers(question):
	url = stackoverflow(question)
	page = requests.get(url)
	data = page.text
	soup = BeautifulSoup(data,'html.parser')
	time.sleep(3)
	soup = soup.find("div", {"class":"search-results"})
	
	try:
		questions = soup.find_all('div', {"class":"result-link"})
		answers = soup.find_all('div', {"class":"excerpt"})

		display_answers(questions, answers)

	except:
		get_answers(question)


question = raw_input("Enter Your Query : ")
get_answers(question)
driver.quit()
