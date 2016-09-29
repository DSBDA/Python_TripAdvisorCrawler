import re
import urllib
from bs4 import BeautifulSoup


class HotelListElement:
    def __init__(self, _Id, _Name, _Href, _ReviewCnt):
        self.Id = _Id
        self.Name = _Name
        self.Href = _Href
        self.ReviewCnt = _ReviewCnt


def run_program(url):
    HrefList = []
    HrefList.append(url)

    req = urllib.request.urlopen(url)
    content = req.read().decode(req.info().get_content_charset())
    city_info = re.findall('Hotels-g(.*?)-(.*?)-Hotels', content)[0]
    print('Crawler City = ' + city_info[0] + '_' + city_info[1])

    soup = BeautifulSoup(content, "html.parser")
    NumberList = soup.find_all('a', attrs={'class': 'pageNum'})

    if NumberList is not None:
        TotalPage = int(NumberList[len(NumberList) - 1].get('data-page-number'))
        SplitString = NumberList[0].get('href').split('-oa30-')
        for i in range(2, TotalPage + 1, 1):
            HrefList.append(DomainName + SplitString[0] + '-oa' + str((i - 1) * 30) + '-' + SplitString[1])

    main_crawler(HrefList)

    HotelList = sorted(TempList, key=lambda HotelListElement: HotelListElement.ReviewCnt, reverse=True)
    TempList.clear()

    return HotelList


def main_crawler(HrefList):
    for url in HrefList:
        req = urllib.request.urlopen(url)
        content = req.read().decode(req.info().get_content_charset())
        soup = BeautifulSoup(content, "html.parser")

        ParserTemp = soup.find_all('a', attrs={'class': 'property_title'})
        ParserReviewNumTemp = soup.find_all('span', attrs={'class': 'more'})

        for i in range(0, len(ParserTemp), 1):
            link = ParserTemp[i]
            Temp_Id = link.get('id').replace('property_', '')
            if Temp_Id not in ScoreList:
                ScoreList.append(Temp_Id)

                if len(ParserTemp) == len(ParserReviewNumTemp):
                    ReviewNum = ParserReviewNumTemp[i].text.replace(",", "").replace(" Reviews", "").replace(" Review",
                                                                                                             "")
                    if int(ReviewNum) < 3000:
                        continue
                else:
                    req = urllib.request.urlopen(DomainName + link.get('href'))
                    content = req.read().decode(req.info().get_content_charset())
                    soup2 = BeautifulSoup(content, "html.parser")

                    Temp_Element = soup2.find('a', attrs={'class': 'more taLnk'})
                    if Temp_Element is not None:
                        ReviewNum = Temp_Element.text.replace(",", "").replace(" Reviews", "").replace(" Review", "")
                        if int(ReviewNum) < 3000:
                            continue
                    else:
                        continue

                Temp_Hotel = HotelListElement(Temp_Id, link.text, 'http://www.tripadvisor.com' + link.get('href'),
                                              int(ReviewNum))
                TempList.append(Temp_Hotel)

DomainName = 'http://www.tripadvisor.com'

HotelList = list()
ScoreList = list()
TempList = list()
