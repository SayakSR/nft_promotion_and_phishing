import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

# def take_screenshot(url_id,url,current_time):

# 	options = webdriver.ChromeOptions()
# 	options.headless = True
# 	#driver = webdriver.Chrome(options=options)
# 	driver = webdriver.Chrome(executable_path='/home/sayaksr/Desktop/chromedriver/chromedriver',options=options)

# 	URL = url

# 	driver.get(URL)

# 	time.sleep(3)

# 	S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
# 	driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
# 	#driver.find_element_by_tag_name('body').screenshot('screens/'+str(iteration)+"/"+str(filename)+'.png') OLD USAGE
# 	driver.find_element('body').screenshot(f'screens/{url_id}_{datestamp}.png')


# 	driver.quit()



def take_screenshot(url_id,url,current_time):

	print(url_id)
	if 'http' not in url:
		url='http://'+url
	

	options = webdriver.ChromeOptions()
	options.headless = True
	#driver = webdriver.Chrome(options=options)
	driver = webdriver.Chrome(executable_path='/home/sayaksr/Desktop/chromedriver/chromedriver',options=options)

	URL = url

	driver.get(URL)

	time.sleep(3)

	driver.save_screenshot(f'screens/original_{url_id}_{current_time}.png')

	driver.quit()
 
	img = Image.open(f'screens/original_{url_id}_{current_time}.png')
	
	I1 = ImageDraw.Draw(img)
	
	myFont = ImageFont.truetype('Lato-Bold.ttf', 20)
	
	I1.text((10, 10), url , fill =(255, 0, 0), font=myFont)
	
	img.save(f'screens/{url_id}_{current_time}.png')

	file_name_string=f"{url_id}_{current_time}.png"

	return file_name_string



# Test

#take_screenshot('12345','http://www.google.com','45783')

