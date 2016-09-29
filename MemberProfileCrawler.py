import re
from bs4 import BeautifulSoup
import time
import Function


class MemeberInfoElement:
    def __init__(self):
        self.Name = '-1'
        self.TotelHelpfulVotes = '-1'
        self.Since = '-1'
        self.Location = '-1'
        self.Age = '-1'
        self.Gender = '-1'
        self.Badge = '-1'

    def setInfo(self, _Name, _TotelHelpfulVotes, _Since, _Location, _Age, _Gender, _Badge):
        self.Name = _Name
        self.TotelHelpfulVotes = _TotelHelpfulVotes
        self.Since = _Since
        self.Location = _Location
        self.Age = _Age
        self.Gender = _Gender
        self.Badge = _Badge


'''
class MemberReviewElement:
    def __init__(self, _Date, _Rating, _Helpful, _Hyperlink):
        self.Date = _Date
        self.Rating = _Rating
        self.Helpful = _Helpful
        self.Hyperlink = _Hyperlink
'''


def run_program(SourceArray, SystemTime):
    print('===MemberProfileCrawler Start====')
    cursor = Function.DatabaseConnectionBuilder()
    for index in SourceArray:
        url = 'http://www.tripadvisor.com/MemberOverlay?uid=' + index[0] + '&c=&src=' + index[
            1] + '&fus=false&partner=false&LsoId='

        try:
            Temp = get_crawlerinfo(url)
            if Temp[0] != 'skip':
                driver.get('http://www.tripadvisor.com/' + Temp[0])
            else:
                continue
            Temp_Name = Temp[1].replace(',', '@[CMA]').replace("'", "''")

            print(Temp_Name)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            All_Page = driver.page_source.replace('\n', '')

            Temp_Info = soup.find_all("a", attrs={'name': 'lists'})
            if len(Temp_Info) != 0:
                if len(Temp_Info) == 1:
                    Temp_TotelHelpfulVotes = Temp_Info[0].text.replace(' Helpful votes', '').replace(' Helpful vote',
                                                                                                     '').replace(' ',
                                                                                                                 '')
                else:
                    for i in range(0, len(Temp_Info), 1):
                        if 'Helpful' in Temp_Info[i]:
                            Temp_TotelHelpfulVotes = Temp_Info[i].text.replace(' Helpful votes', '').replace(
                                ' Helpful vote',
                                '').replace(' ', '')
            else:
                Temp_TotelHelpfulVotes = '-1'

            try:
                PreText = soup.find('p', attrs={'class': 'since'}).text.replace('Since ', '')

                year = PreText.split(' ')[1]
                month = PreText.split(' ')[0]

                if month == 'Jan':
                    month = '1'
                elif month == 'Feb':
                    month = '2'
                elif month == 'Mar':
                    month = '3'
                elif month == 'Apr':
                    month = '4'
                elif month == 'May':
                    month = '5'
                elif month == 'Jun':
                    month = '6'
                elif month == 'Jul':
                    month = '7'
                elif month == 'Aug':
                    month = '8'
                elif month == 'Sep':
                    month = '9'
                elif month == 'Oct':
                    month = '10'
                elif month == 'Nov':
                    month = '11'
                elif month == 'Dec':
                    month = '12'

                Temp_Since = year + '-' + month + '-1'
                time.strptime(Temp_Since, "%Y-%m-%d")
            except:
                Temp_Since = '1900-1-1'

            Temp_Info = soup.find('div', attrs={'class', 'hometown'})
            if len(Temp_Info) != 0:
                Temp_Location = Temp_Info.text.replace(',', '@[CMA]').replace("'", "''")
            else:
                Temp_Location = '-1'

            Temp_Info = re.findall(',"age":(.*?),', All_Page)  # 抓不到，代表未公開，設為0,年齡屬性為0~6
            if len(Temp_Info) != 0:
                Temp_Age = Temp_Info[0]
            else:
                Temp_Age = '-1'

            Temp_Info = re.findall('"gender":"(.*?)"', All_Page)  # male : 0 ; female : 1
            if len(Temp_Info) != 0:
                if Temp_Info[0] == 'male':
                    Temp_Gender = '0'
                else:
                    Temp_Gender = '1'
            else:
                Temp_Gender = '-1'

            cursor.execute("SELECT * FROM MemberInfo WHERE UserId='" + index[
                0] + "' AND TotalHelpfulVote='" + Temp_TotelHelpfulVotes + "' AND Name='" + Temp_Name + "' AND Gender='" + Temp_Gender + "' AND Age='" + Temp_Age + "' AND Location='" + Temp_Location + "' AND Since='" + Temp_Since + "'")
            CheckQuery = cursor.fetchall()

            if len(CheckQuery) == 0 or CheckQuery is None:
                cursor.execute(
                    "INSERT INTO MemberInfo(UserId,TotalHelpfulVote, Name ,Gender,Age,Location,Since,TimeStamp) values ('" +
                    index[
                        0] + "', '" + Temp_TotelHelpfulVotes + "', '" + Temp_Name + "','" + Temp_Gender + "','" + Temp_Age + "','" + Temp_Location + "','" + Temp_Since + "','" + SystemTime + "')")
                cursor.commit()
        except:
            continue

def get_crawlerinfo(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        userurl = soup.find('a').get('href')
        returnvalue = soup.find('h3', attrs={'class': 'username'}).text
    except:
        userurl = 'skip'
        returnvalue = 'skip'
    return userurl, returnvalue


#driver = Function.BrowserSetting2()
driver = Function.BrowserSetting()
