# coding=utf-8

import urllib.request
import re
import urllib
from bs4 import BeautifulSoup
import ContentCrawler
import Function
import datetime


class ReviewElement:
    def __init__(self, _HotelId, _ReviewId, _UserId, _AtPage, _OrderOfPage, _ReviewDate, _TimeStamp):
        self.HotelId = _HotelId
        self.ReviewId = _ReviewId
        self.UserId = _UserId
        self.AtPage = _AtPage
        self.OrderOfPage = _OrderOfPage
        self.ReviewDate = _ReviewDate
        self.TimeStamp = _TimeStamp


class ContentElement:
    def __init__(self, _ReviewId, _ReviewTitle, _ReviewRating, _RatingDate, _ReviewContent, _ReviewHelpfulvotes):
        self.ReviewId = _ReviewId
        self.ReviewTitle = _ReviewTitle
        self.ReviewRating = _ReviewRating
        self.ReviewContent = _ReviewContent
        self.ReviewHelpfulvotes = _ReviewHelpfulvotes


def run_program(url, hotelid, areaid, SystemTime, delta):
    HotelReviewList.clear()
    ReviewContentList.clear()
    cursor = Function.DatabaseConnectionBuilder()

    while 1:
        try:
            driver.get(url)
            break
        except:
            driver.refresh()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    LinkSelect = soup.find_all('a', attrs={'class': 'pageNum'})
    PageCount = 1

    if len(LinkSelect) != 0:
        TempLink = DomainName + LinkSelect[0].get('href')
        global SplitTempLink
        SplitTempLink = TempLink.split('or10')
        PageCount = int(re.findall('-or(.*?)0-', LinkSelect[len(LinkSelect) - 1].get('href'))[0]) + 1

    print('Total Page=' + str(PageCount))
    Element = main_crawler("1", soup, hotelid, areaid, SystemTime, cursor, delta)

    if Element is not False:

        ReviewCnt = len(HotelReviewList)
        print('Page 1 is Done And Count= ' + str(ReviewCnt))
        if ReviewCnt >= 10 and PageCount > 1:
            for i in range(1, PageCount, 1):
                if len(HotelReviewList) == delta:
                    break
                driver.get(SplitTempLink[0] + 'or' + str(i) + '0' + SplitTempLink[1])
                # req = urllib.request.urlopen(SplitTempLink[0] + 'or' + str(i) + '0' + SplitTempLink[1])
                # content = req.read().decode(req.info().get_content_charset())
                soup = BeautifulSoup(driver.page_source, "html.parser")

                main_crawler(str(i + 1), soup, hotelid, areaid, SystemTime, cursor, delta)
                if len(HotelReviewList) - ReviewCnt == 0:
                    break
                print('Page ' + str(i + 1) + ' is Done And Count= ' + str(len(HotelReviewList) - ReviewCnt))

                ReviewCnt = len(HotelReviewList)

    return HotelReviewList, ReviewContentList, TravelList


def main_crawler(ThisPage, soup, hotelid, areaid, SystemTime, cursor, delta):
    SoupTemp = soup.find_all('div', attrs={'class': 'reviewSelector'})

    OrderNum = 1
    if SoupTemp is not None:
        for index in SoupTemp:
            if len(HotelReviewList) == delta:
                return False

            ReviewId = index.get('id').replace('review_', '')

            # check database, if[hotelid]&[reivewid] can query just copy the
            # data information and insert new record.
            cursor.execute(
                "SELECT UserId, TimeStamp FROM ReviewOverview WHERE HotelId='" + hotelid + "' AND ReviewId='" + ReviewId + "'")
            row = cursor.fetchall()

            if len(row) != 0:
                if str(row[len(row) - 1][1]) == SystemTime:
                    continue
                UserId = row[len(row) - 1][0]
            # check end

            else:
                UserId = '-1'
                Temp_Info = re.findall('"UID_(.*?)-SRC_(.*?)"', str(index).replace('\n', ''))

                if len(Temp_Info) != 0:
                    UserId = Temp_Info[0][0]

                if UserId == '-1':

                    CheckUrl = 'http://www.tripadvisor.com/ExpandedUserReviews-g' + areaid + '-d' + hotelid + '?target=' + ReviewId + '&context=1&reviews=' + ReviewId
                    driver.get(CheckUrl)
                    # CheckReq = urllib.request.urlopen(CheckUrl)
                    # CheckContent = CheckReq.read().decode(CheckReq.info().get_content_charset())
                    SplitContent = driver.page_source.replace('\n', '').replace('"', '')
                    TempArray = re.findall('<div class=member_info>(.*?)<div class=member_info>', SplitContent)

                    if len(TempArray) == 0:
                        TempArray = [(SplitContent)]
                    TempArray2 = re.findall('UID_(.*?)-SRC_(.*?)$', TempArray[0])
                    if len(TempArray2) != 0:
                        UserId = TempArray2[0][0]

                        # _HotelId, _ReviewId, _UserId, _AtPage, _OrderOfPAge, _ReviewDate, _TimeStamp)
            ContentUrl = 'http://www.tripadvisor.com/ExpandedUserReviews-g' + areaid + '-d' + hotelid + '?target=' + ReviewId + '&context=1&reviews=' + ReviewId
            ReviewContent = ContentCrawler.content_crawler(ContentUrl, UserId)
            Dict = ReviewContent[1]
            ReviewContent = ReviewContent[0]
            tempDate = datetime.datetime.strptime(ReviewContent.RatingDate, "%Y-%m-%d").date()
            if tempDate > datetime.datetime.strptime('2016-4-1', "%Y-%m-%d").date():
                Temp_ReviewElement = ReviewElement(hotelid, ReviewId, UserId, ThisPage, OrderNum,
                                                   ReviewContent.RatingDate, SystemTime)

                HotelReviewList.append(Temp_ReviewElement)
                soup2 = BeautifulSoup(index.prettify(), "html.parser")
                Parti = soup2.select('.entry > .partial_entry')

                if len(Parti) != 0:
                    ReviewContent.Partial = re.sub('\s+', ' ', Parti[0].text.replace('\n', ''))
                ReviewContentList.append(ReviewContent)
                TravelList.append({'hotelid':hotelid, 'ReviewId':ReviewId,'TravelMonth':Dict['TravelMonth'],'TravelType':Dict['TravelType'],'PhotoCnt':Dict['PhotoCnt']})
                OrderNum += 1

            else:
                break

        return True
    else:
        return False


DomainName = 'http://www.tripadvisor.com'
HotelReviewList = list()
ReviewContentList = list()
TravelList = list()
content = ""
SplitTempLink = []
driver = Function.BrowserSetting()
