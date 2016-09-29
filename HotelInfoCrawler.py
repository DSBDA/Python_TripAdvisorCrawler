import urllib.request
import re
import Function
from bs4 import BeautifulSoup


class HotelInfoElement:
    # data structure
    def __init__(self, _id, _hRank, _hRating, _hStarClass, _hRoomNum, _hReviewNum, _excellent, _verygood, _average,
                 _poor, _terrible, _hFamilies, _hCouples, _hSolo, _hBusiness, _hFrineds, _hMarMay, _hJunAug, _hSepNov,
                 _hDecFeb, ):
        self.Id = _id
        self.hRank = _hRank
        self.hRating = _hRating
        self.hStarClass = _hStarClass
        self.hRoomNum = _hRoomNum
        self.hReviewNum = _hReviewNum
        self.excellent = _excellent
        self.verygood = _verygood
        self.average = _average
        self.poor = _poor
        self.terrible = _terrible
        self.hFamilies = _hFamilies
        self.hCouples = _hCouples
        self.hSolo = _hSolo
        self.hBusiness = _hBusiness
        self.hFrineds = _hFrineds
        self.hMarMay = _hMarMay
        self.hJunAug = _hJunAug
        self.hSepNov = _hSepNov
        self.hDecFeb = _hDecFeb


def run_program(hotellist):
    print('HOTEL COUNT= ' + str(len(hotellist)))
    for index in hotellist:
        main_crawler(index[4])  # INDEX[4]=URL

    return ResultList


def main_crawler(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    '''
    req = urllib.request.urlopen(url)
    content = req.read().decode(req.info().get_content_charset())
    soup = BeautifulSoup(content, "html.parser")
    '''
    ID = re.findall('-d(.*?)-', url)[0]

    try:
        Temp_Element = soup.find('b', attrs={'class': 'rank'})
        if Temp_Element is not None:
            hRank = Temp_Element.text.replace('#', '')
        else:
            hRank = '-1'

        Temp_Element = soup.find('img', attrs={'class': 'sprite-rating_rr_fill'})
        if Temp_Element is not None:
            hRating = re.findall('content="(.*?)"', str(Temp_Element))[0]
        else:
            hRating = '-1'

        Temp_Element = soup.find('div', attrs={'class': 'additional_info stars'})
        if Temp_Element is not None:
            hStarClass = re.findall('Hotel Class:(.*?) star', Temp_Element.text)[0]
        else:
            hStarClass = '-1'

        Temp_Element = soup.find('span', attrs={'class': 'tabs_num_rooms'})
        if Temp_Element is not None:
            hRoomNum = Temp_Element.text.replace(' ', '')
        else:
            hRoomNum = '-1'

        Temp_Element = soup.find('a', attrs={'class': 'more taLnk'})
        if Temp_Element is not None:
            hReviewNum = Temp_Element.text.replace(' Reviews', '').replace(' Review', '')
        else:
            hReviewNum = '-1'

        Temp_Element = soup.find('div', attrs={'id': 'ratingFilter'})
        if Temp_Element is not None:
            Temp_Rating = Temp_Element.text.replace('\n', '').replace('Traveler rating', '').replace(' ', '')
            excellent = re.findall('Excellent(.*?)Very', Temp_Rating)[0]
            verygood = re.findall('Verygood(.*?)Average', Temp_Rating)[0]
            average = re.findall('Average(.*?)Poor', Temp_Rating)[0]
            poor = re.findall('Poor(.*?)Terrible', Temp_Rating)[0]
            terrible = re.findall('Terrible(.*?)$', Temp_Rating)[0]
        else:
            excellent = '-1'
            verygood = '-1'
            average = '-1'
            poor = '-1'
            terrible = '-1'

        Temp_Element = soup.find('div', attrs={'class': 'col segment '})
        if Temp_Element is not None:
            Temp_Rating = Temp_Element.text.replace('\n', '').replace('Traveler type', '').replace('(', '').replace(')',
                                                                                                                    '').replace(
                ' ', '')
            hFamilies = re.findall('Families(.*?)Couples', Temp_Rating)[0]
            hCouples = re.findall('Couples(.*?)Solo', Temp_Rating)[0]
            hSolo = re.findall('Solo(.*?)Business', Temp_Rating)[0]
            hBusiness = re.findall('Business(.*?)Friends', Temp_Rating)[0]
            hFrineds = re.findall('Friends(.*?)$', Temp_Rating)[0]
        else:
            hFamilies = '-1'
            hCouples = '-1'
            hSolo = '-1'
            hBusiness = '-1'
            hFrineds = '-1'

        Temp_Element = soup.find('div', attrs={'class': 'col season '})
        if Temp_Element is not None:
            Temp_Rating = Temp_Element.text.replace('\n', '').replace('Time of year', '').replace('(', '').replace(')',
                                                                                                                   '').replace(
                ' ', '')
            hMarMay = re.findall('Mar-May(.*?)Jun-Aug', Temp_Rating)[0]
            hJunAug = re.findall('Jun-Aug(.*?)Sep-Nov', Temp_Rating)[0]
            hSepNov = re.findall('Sep-Nov(.*?)Dec-Feb', Temp_Rating)[0]
            hDecFeb = re.findall('Dec-Feb(.*?)$', Temp_Rating)[0]
        else:
            hMarMay = '-1'
            hJunAug = '-1'
            hSepNov = '-1'
            hDecFeb = '-1'
    except:
        print('[System]occur exception in HotelInfoCrawler, please check!')
        SystemExit(0)

    Temp_Info = HotelInfoElement(ID, hRank, hRating, hStarClass, hRoomNum, hReviewNum, excellent, verygood, average,
                                 poor, terrible, hFamilies, hCouples, hSolo, hBusiness, hFrineds, hMarMay, hJunAug,
                                 hSepNov, hDecFeb)

    ResultList.append(Temp_Info)
    print("=== " + ID + " is done  ====")


ResultList = list()
driver = Function.BrowserSetting()

