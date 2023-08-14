from bs4 import BeautifulSoup
from urllib.request import urlretrieve, urlopen
import requests
#import urllib

# use this image scraper from the location that 
#you want to save scraped images to

def make_soup(url):
    html = requests.get(url).text
    return BeautifulSoup(html, 'html.parser')

def get_images(url):
    soup = make_soup(url)
    #this makes a list of bs4 element tags
    images = [img for img in soup.findAll('img')]
    print(soup)
    print(str(len(images)) + "images found.")
    print('Downloading images to current working directory.')
    #compile our unicode list of image links
    image_links = [each.get('src') for each in images]
    for each in image_links:
        filename=each.split('/')[-1]
        urlretrieve(each, filename)
    return image_links

#a standard call looks like this
get_images('https://manhua.dmzj.com/beatstars/71089.shtml#@page=1')
