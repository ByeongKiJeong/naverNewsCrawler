import datetime
import urllib
import time
import json
import sys
import os
import re

from bs4 import BeautifulSoup

from Crawler import Crawler

reload(sys)
sys.setdefaultencoding('utf8')

class NewsArticle(object):

    def __init__(self):
        self.title = ''
        self.date = ''
        self.time = ''
        self.press = ''
        self.contents = ''

    def get_article(self, url):
        crawler = Crawler()
        # get html data from url
        web_data = crawler.get_page(url)
        soup = BeautifulSoup(web_data, 'html.parser')

        # remove link news 
        [e.extract() for e in soup('div', {'class':'link_news'})]

        # article title
        self.title = soup('h3', {'id':'articleTitle'})[0].text

        # create date and time of article
        date_time = soup('span', {'class':'t11'})[0].text.split()
        self.date = date_time[0]
        self.time = date_time[1]

        # press name
        press_logo = soup('div', {'class':'press_logo'})[0]
        self.press = press_logo.find('img')['alt']
        del press_logo

        # article contents
        self.contents = soup('div', {'id':'articleBodyContents'})[0].text
        self.contents = re.sub('[\n\r]', '', self.contents)

    def write_as_json(self):
        return json.dumps(self.write_as_dict())

    def write_as_dict(self):
        json_data = {
            'title':self.title,
            'date':self.date,
            'time':self.time,
            'press':self.press,
            'contents':self.contents
            }
        return json_data
def get_list(section, date):

    # NAVER news url
    naver_news_url = 'http://news.naver.com/main/list.nhn'
    naver_news_parameter = {'mode':'LSD', 'mid':'sec', 'sid1':'', 'date':date, 'page':''}
    naver_news_parameter['sid1'] = section

    page = 1
    url_list = []
    while True:
        naver_news_parameter['page'] = page
        url =  naver_news_url + '?' + urllib.urlencode(naver_news_parameter)
        
        # get html data
        crawler = Crawler()
        web_data = crawler.get_page(url)
        
        # html parsing
        soup= BeautifulSoup(web_data, 'html.parser')
        list_body = soup('div', {'class':'list_body newsflash_body'})[0]

        # get each article's url
        list_body = list_body.findAll('li')
        current_list = []
        for e in list_body:
            current_list.append(e.find('a')['href'])
        del list_body
        
        # break when current page is end of url list
        if current_list[0] in url_list:
            break

        # add to url list
        url_list += current_list

        # next url page
        page += 1

    return url_list
        
        
def news_crawling(section, date):

    # set section as dictionary
    section_name = ['politic', 'economy', 'society', 'life/culture','world', 'it/ science', 'entertainment', 'sports', 'opinion']
    section_no = ['100', '101', '102', '103', '104', '105', '106', '107', '110']
    sections = zip(section_name, section_no)
    sections = dict(sections)

    # get news url list
    url_list = get_list(sections[section], date)
    article_data = []

    for url in url_list:
        try:
            news_article = NewsArticle()
            news_article.get_article(url)
            article_data.append(news_article.write_as_dict())

        except IndexError, err_msg:
            with open(date + '_' + section.replace('/', '_')+'_log.log', 'a') as f:
                f.write('[error] ' + err_msg.message +' | ' + url +  '\n')
        
    with open(date + '_' + section.replace('/', '_')+'.json', 'w') as f:
        json.dump(article_data, f, ensure_ascii = False, indent = True)


if __name__ == '__main__':
    strDate = sys.argv[1]
    endDate = sys.argv[2]

    date = datetime.date(int(strDate[0:4]), int(strDate[4:6]), int(strDate[6:8]))
    enddate = datetime.date(int(endDate[0:4]), int(endDate[4:6]), int(endDate[6:8]))
    timeDiff = enddate -date

    section_name = ['politic', 'economy', 'society', 'life/culture', 'world', 'it/ science', 'entertainment', 'sports', 'opinion']
    """
    for section in section_name:
        if section.replace('/', '_') not in os.listdir('.'):
            os.mkdir(section.replace('/', '_'))
        os.chdir(section.replace('/', '_'))
        for delta_day in xrange(int(timeDiff.days)):
            dates = date + datetime.timedelta(delta_day)
            dates = dates.isoformat()
            dates = dates.replace('-', '')
            print dates +' ' + section +' crawling'
            
            news_crawling(section, dates)
        os.chdir('..')
    """
    for section in section_name:
        if section.replace('/', '_') not in os.listdir('.'):
            os.mkdir(section.replace('/', '_'))
        
    for delta_day in xrange(int(timeDiff.days) + 1):
        for section in section_name:
            os.chdir(section.replace('/', '_'))

            dates = date + datetime.timedelta(delta_day)
            dates = dates.isoformat()
            dates = dates.replace('-', '')
            print dates +' ' + section +' crawling'
            
            news_crawling(section, dates)
            os.chdir('..')
