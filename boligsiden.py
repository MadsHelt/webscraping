
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

driver.get("https://www.boligsiden.dk/salgspris/arkiv/alle/1?periode.from=2012-01-01&kommune=aarhus&sortdescending=true&sort=udbudt") 

csv_file = open('boligsiden.csv', 'w')
# Windows users need to open the file using 'wb'
# csv_file = open('reviews.csv', 'wb')
writer = csv.writer(csv_file)
writer.writerow(['typehus', 'grund', 'postnummer', 'adresse', 'vaerelse', 'href', 'energimaerke']) 

index = 1
while True:
	time.sleep(2)
	try:
		print("Scraping Page number " + str(index))
		index = index + 1

		# Find all the reviews.
		reviews = driver.find_elements_by_xpath('//div[@class="card card-item card-item--property card-item--archive"]')
		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Use Xpath to locate the title, content, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			adresse = review.find_element_by_xpath('.//div[@class="info__address"]/h3/a').text.encode('utf-8')
			#print(adresse)
			postnummer = review.find_element_by_xpath('.//div[@class="info__address"]/div').text.encode('utf-8')
			#print(postnummer)
			typehus = review.find_element_by_xpath('.//div[@class="info__address"]/div[2]').text.encode('utf-8')
			#print(typehus)
			grundareal = review.find_element_by_xpath('.//ul[@class="card__kf"]//li[@class="areaparcel"]').text.encode('utf-8').strip()
			#print(grundareal)
			vaerelse = review.find_element_by_xpath('.//ul[@class="card__kf"]/li[@class="numberofrooms"]').text.encode('utf-8').strip()
			#print(vaerelse)
			href = review.find_element_by_class_name("extra").find_element_by_tag_name('a').get_attribute('href')

			try:
				energimaerke = review.find_element_by_class_name('info__address').find_element_by_tag_name('div').find_element_by_tag_name('a').get_attribute('class')
			except:
				energimaerke = ''
			print(energimaerke)

			review_dict['adresse'] = adresse
			review_dict['postnummer'] = postnummer
			review_dict['typehus'] = typehus
			review_dict['grundareal'] = grundareal
			review_dict['vaerelse'] = vaerelse
			review_dict['href'] = href
			review_dict['energimaerke'] = energimaerke
			writer.writerow(review_dict.values())

		# Locate the next button on the page.
		button = driver.find_element_by_xpath('//div[@class="pagenumber"]/a[2]') 
		driver.execute_script("arguments[0].click();", button) # Remember that the button should be in the for loop (because it's in the same column)
		button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break
