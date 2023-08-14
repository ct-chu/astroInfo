from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, ContentTooShortError
import requests
from bs4 import BeautifulSoup
import feedparser
import re

# BesutifulSoup

##link_list = ['https://www.lightnovel.cn/forum-141-1.html',\
##             'https://www.lightnovel.cn/forum-141-2.html',\
##             'https://www.lightnovel.cn/forum-141-3.html',\
##             'https://www.lightnovel.cn/forum-141-4.html',\
##             'https://www.lightnovel.cn/forum-141-5.html',\
##             'https://www.lightnovel.cn/forum-141-6.html',\
##             'https://www.lightnovel.cn/forum-141-7.html',\
##             'https://www.lightnovel.cn/forum-141-8.html',\
##             'https://www.lightnovel.cn/forum-141-9.html',\
##             'https://www.lightnovel.cn/forum-141-10.html']

link_list = ['https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2',\
             'https://www.lightnovel.us/category/33/0?type=2']

with open('comic_LK.txt', 'r+', encoding='utf-8') as text_file:
    data = text_file.read() # f.read() won't go back to begining, write it to new string

    # check for each page
    
    link_0 = link_list[0]
    html_0 = requests.get(link_0).text
    soup_0 = BeautifulSoup(html_0, 'html.parser')
    title_list_0 = soup_0.find_all('a',class_='s xst')
      
    for i in range(len(title_list_0)):
        if title_list_0[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_0[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_0[i].get('href')))
    print('^P.1')
        
    link_1 = link_list[1]
    html_1 = requests.get(link_1).text
    soup_1 = BeautifulSoup(html_1, 'html.parser')
    title_list_1 = soup_1.find_all('a',class_='s xst')

    for i in range(len(title_list_1)):
        if title_list_1[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_1[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_1[i].get('href')))
    print('^P.2')

    link_2 = link_list[2]
    html_2 = requests.get(link_2).text
    soup_2 = BeautifulSoup(html_2, 'html.parser')
    title_list_2 = soup_2.find_all('a',class_='s xst')

    for i in range(len(title_list_2)):
        if title_list_2[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_2[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_2[i].get('href')))
    print('^P.3')

    link_3 = link_list[3]
    html_3 = requests.get(link_3).text
    soup_3 = BeautifulSoup(html_3, 'html.parser')
    title_list_3 = soup_3.find_all('a',class_='s xst')

    for i in range(len(title_list_3)):
        if title_list_3[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_3[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_3[i].get('href')))
    print('^P.4')

    link_4 = link_list[4]
    html_4 = requests.get(link_4).text
    soup_4 = BeautifulSoup(html_4, 'html.parser')
    title_list_4 = soup_4.find_all('a',class_='s xst')

    for i in range(len(title_list_4)):
        if title_list_4[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_4[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_4[i].get('href')))
    print('^P.5')

    link_5 = link_list[5]
    html_5 = requests.get(link_5).text
    soup_5 = BeautifulSoup(html_5, 'html.parser')
    title_list_5 = soup_5.find_all('a',class_='s xst')

    for i in range(len(title_list_5)):
        if title_list_5[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_5[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_5[i].get('href')))
    print('^P.6')

    link_6 = link_list[6]
    html_6 = requests.get(link_6).text
    soup_6 = BeautifulSoup(html_6, 'html.parser')
    title_list_6 = soup_6.find_all('a',class_='s xst')

    for i in range(len(title_list_6)):
        if title_list_6[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_6[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_6[i].get('href')))
    print('^P.7')

    link_7 = link_list[7]
    html_7 = requests.get(link_7).text
    soup_7 = BeautifulSoup(html_7, 'html.parser')
    title_list_7 = soup_7.find_all('a',class_='s xst')

    for i in range(len(title_list_7)):
        if title_list_7[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_7[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_7[i].get('href')))
    print('^P.8')

    link_8 = link_list[8]
    html_8 = requests.get(link_8).text
    soup_8 = BeautifulSoup(html_8, 'html.parser')
    title_list_8 = soup_8.find_all('a',class_='s xst')

    for i in range(len(title_list_8)):
        if title_list_8[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_8[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_8[i].get('href')))
    print('^P.9')

    link_9 = link_list[9]
    html_9 = requests.get(link_9).text
    soup_9 = BeautifulSoup(html_9, 'html.parser')
    title_list_9 = soup_9.find_all('a',class_='s xst')

    for i in range(len(title_list_9)):
        if title_list_9[i].text.replace('[连载]', '').rsplit('[', 1)[0] in data:
            pass
        else:
            print(title_list_9[i].text.replace('[连载]', '').rsplit('[', 1)[0])
            print('https://www.lightnovel.cn/'+str(title_list_9[i].get('href')))
    print('^P.10')

# export to text file
    for i in title_list_0:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)
        
    for i in title_list_1:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)
    
    for i in title_list_2:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_3:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_4:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_5:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_6:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_7:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_8:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

    for i in title_list_9:
        print(i.text.replace('[连载]', '').rsplit('[', 1)[0], file=text_file)
        print('https://www.lightnovel.cn/'+str(i.get('href')), file=text_file)
        print('', file=text_file)

