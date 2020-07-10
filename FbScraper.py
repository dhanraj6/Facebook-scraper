from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import bs4
import pandas as pd

a=int(input("Enter the no of scrolls you want to perform: "))
def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#add your chromedriver path
driver = webdriver.Chrome("your chrome driver path")

#add the facebook page link whose data you want to scrape
driver.get('https://www.facebook.com/pg/abc/reviews/?ref=page_internal')

driver.maximize_window()
time.sleep(3)
htmlstring = driver.page_source
afterstring = ""
for i in range(1,(a+1)):
    print("scroll "+str(i)+" finished")
    afterstring = htmlstring
    scroll()
    htmlstring = driver.page_source
    if afterstring == htmlstring:
        scroll()
        htmlstring = driver.page_source
        if afterstring == htmlstring:
            print("--Scrapping End--")
            break
    time.sleep(3)
soup = BeautifulSoup(htmlstring, "html.parser")
counter = 0
Reviwer_data = {'Reviewer Name':[],'Reviewer Rating': [], 'Reviewer Profile URL': [], 'Review': [], 'Time': []}
for i in soup.find_all(class_='_5pcr userContentWrapper'):
    e = i.find(class_="clearfix y_c3pyo2ta3")
    e1 = e.get('title')
    if(i.find('a').get('title')):
        Reviwer_data['Reviewer Name'].append(i.find('a').get('title'))
    elif(e1):
        Reviwer_data['Reviewer Name'].append(e.get('title'))
    else:
        Reviwer_data['Reviewer Name'].append(e.find('span').get('title'))
    Reviwer_data['Reviewer Rating'].append(i.find('u'))
    l=i.find(class_='fsm fwn fcg')
    Reviwer_data['Reviewer Profile URL'].append('https://www.facebook.com'+l.find('a').get('href'))
    Reviwer_data['Review'].append(i.find('p'))
    Reviwer_data['Time'].append(i.find(class_="timestampContent").get_text())
    counter = counter + 1
print("Total reviews scraped:" + str(counter))
pd.DataFrame(Reviwer_data).to_csv('reviews.csv', index=0)
