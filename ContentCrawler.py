# coding=utf-8

import urllib.request
import re
import Function
from bs4 import BeautifulSoup


class ContentElement:
    def __init__(self, _ReviewId, _ReviewTitle, _ReviewRating, _RatingDate, _ReviewContent, _ReviewHelpfulvotes):
        self.ReviewId = _ReviewId
        self.ReviewTitle = _ReviewTitle
        self.ReviewRating = _ReviewRating
        self.RatingDate = _RatingDate
        self.Partial = 'not yet'
        self.ReviewContent = _ReviewContent
        self.ReviewHelpfulvotes = _ReviewHelpfulvotes


def content_crawler(url, UserId):
    while 1:
        try:
            driver.get(url)
            break
        except:
            driver.refresh()
    # req = urllib.request.urlopen(url)
    # content = req.read().decode(req.info().get_content_charset())
    soup = BeautifulSoup(driver.page_source, "html.parser")
    Check_RId = re.findall('reviews=(.*)', url)[0]
    # if UserId == Check_UId and Check_RId in url:

    Temp_Element = soup.find('span', attrs={'class': 'noQuotes'})
    if Temp_Element is not None:
        title = Temp_Element.text
    else:
        title = '-1'

    Temp_Element = soup.select('.reviewItemInline > span > img')
    if len(Temp_Element) != 0:
        rating = re.findall('(.*?) of 5 stars', soup.select('.reviewItemInline > span > img')[0]['alt'])[0]
    else:
        rating = '-1'
    print(url + ' ' + rating)

    Temp_Element = soup.find('span', attrs={'class': 'ratingDate'})
    if Temp_Element is not None:
        if Temp_Element.get('title') is not None:
            TempDate = Temp_Element.get('title')
        else:
            TempDate = Temp_Element.contents[0].replace('Reviewed ', '').replace('\n', '')
    else:
        TempDate = '-1'

    year = TempDate.split(',')[1].replace(' ', '')
    monthandday = TempDate.split(',')[0]
    month = monthandday.split(' ')[0].replace(' ', '')

    if month == 'January':
        month = '1'
    elif month == 'February':
        month = '2'
    elif month == 'March':
        month = '3'
    elif month == 'April':
        month = '4'
    elif month == 'May':
        month = '5'
    elif month == 'June':
        month = '6'
    elif month == 'July':
        month = '7'
    elif month == 'August':
        month = '8'
    elif month == 'September':
        month = '9'
    elif month == 'October':
        month = '10'
    elif month == 'November':
        month = '11'
    elif month == 'December':
        month = '12'

    day = monthandday.split(' ')[1].replace(' ', '')
    date = year + '-' + month + '-' + day

    Temp_Element = soup.find('div', attrs={'class': 'entry'})
    if Temp_Element is not None:
        content = Temp_Element.text.replace('\n', '').replace('"', '')
    else:
        content = '-1'

    Temp_Element = soup.select('.numHlp')
    if len(Temp_Element) != 0:
        helpfulvote = Temp_Element[0].text.replace('\n', '')
    else:
        helpfulvote = '0'

    Temp_Info = ContentElement(Check_RId, title, rating, date, content, helpfulvote)

    Temp_Element = soup.select('.recommend-titleInline')[0].text

    if 'Stayed' in Temp_Element:
        TravelMonth = Temp_Element.split(',')[0].replace('Stayed ','')
    else:
        TravelMonth = '-1'

    if 'traveled' in Temp_Element:
        TravelType = Temp_Element.split(' ')[-1]
    else:
        TravelType = -1

    Temp_Element = soup.select('.fkASDF')
    PhotoCnt='-1'
    if len(Temp_Element)!=0:
        PhotoCnt=len(Temp_Element)
    return Temp_Info, {'TravelMonth': TravelMonth, 'TravelType': TravelType,'PhotoCnt':PhotoCnt}
    # else:
    #    print('Can not find the review')


driver = Function.BrowserSetting()
