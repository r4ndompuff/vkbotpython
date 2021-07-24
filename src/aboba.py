from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions  
from time import sleep

def getYAML(text, style):
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.headless=True
	chromeOptions.add_argument('--no-sandbox')

	urlAuth = "https://yandex.ru/lab/yalm?style="+style
	driver = webdriver.Chrome("./dict/chromedriver", options=chromeOptions)
	driver.get(urlAuth)
	sleep(2)
	element = driver.find_element_by_xpath('/html/body/article/div/div/button')
	element.click()
	sleep(1)
	element = driver.find_element_by_xpath('/html/body/article/div/div[2]/div[3]/span/span[2]/textarea')
	element.send_keys(text)
	sleep(1)
	element = driver.find_element_by_xpath('/html/body/article/div/div[2]/button')
	driver.execute_script("arguments[0].click();", element)
	sleep(1)
	for i in range(39):
		try:
			element = driver.find_element_by_xpath('/html/body/article/div/div[3]/div/div[1]/span[2]')
			break
		except:
			sleep(1)
	return text + ' ' + element.text