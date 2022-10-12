from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import copy

#you insert the location your webdriver is located
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # give it an excecutable path
time.sleep(15)

#store the html locally to minimize requests
for page in range(1,25):
    wd.get(f"https://www.amazon.co.uk/s?i=electronics&bbn=560798&rh=n%3A310193011&fs=true&page={page}&qid=1664107795&ref=sr_pg_{page}")
    time.sleep(5)
    
    with open(f'html1/{page}.html', 'w') as f:
        f.write(wd.page_source)

#incase there are changes made to the link the number of pages have to be adjusted with it


name = []
price = []
rating = []
number_of_reviews = []

for page in range(1,25):
    #read the files stored locally
    with open(f'html1/{page}.html') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
    
    #for loop to get data from each product on a page
    #try and except incase there are blanks
    for n in range(1,29):
        try:
            name.append(soup.find_all("h2", {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})[n].text)
        except:
            name.append('No name')
        try:
            price.append(soup.find_all('span', {'class':'a-offscreen'})[n].text)
        except:
            price.append('No price')
        try:
            rating.append(soup.find_all('span', {'class':'a-icon-alt'})[n].text)
        except:
            rating.append('No rating')
        try:
            number_of_reviews.append(soup.find_all('span', {'class':'a-size-base s-underline-text'})[n].text)
        except:
            number_of_reviews.append('No reviews')

df = pd.DataFrame(data={'name':name, 'price':price, 'rating':rating, 'number_of_reviews':number_of_reviews})
df1 = df.copy()

#drop empty rows
drp = range(70, 651)
df1 = df1.drop(drp)

#save the data as a json file
df1.to_json('amazon_heaphones_sample3.json')
