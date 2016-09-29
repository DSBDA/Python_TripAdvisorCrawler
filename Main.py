# coding=utf-8

import HotelInfoCrawler  # step 1
import HotelReviewCrawler  # step 2
import MemberProfileCrawler  # step 3
import Function
import re
import datetime


# Step 1
# =================================================================================================================================================================
def Start_HotelInfoCrawler(list):
    HotelInfoList = HotelInfoCrawler.run_program(list)

    # Insert to Database
    for index in HotelInfoList:
        _HotelId = index.Id.replace(',', '')
        _hRank = int(index.hRank.replace(',', ''))
        _hRating = float(index.hRating.replace(',', ''))
        _hStarClass = float(index.hStarClass.replace(',', ''))
        _hRoomNum = int(index.hRoomNum.replace(',', ''))
        _hReviewNum = int(index.hReviewNum.replace(',', ''))

        try:
            sql = "INSERT INTO HotelMain(HotelId, hRank,hRating,hStarClass,hRoomNum,hReviewNum,TimeStamp) values ('{}','{}','{}','{}','{}','{}','{}')"
            sql = sql.format(_HotelId, _hRank, _hRating, _hStarClass, _hRoomNum, _hReviewNum, SystemTime)
            print(' [Insert] {}'.format(sql))
            cursor.execute(sql)
            cursor.commit()
        except:
            print(sql)

        _excellent = int(index.excellent.replace(',', ''))
        _verygood = int(index.verygood.replace(',', ''))
        _average = int(index.average.replace(',', ''))
        _poor = int(index.poor.replace(',', ''))
        _terrible = int(index.terrible.replace(',', ''))
        _hFamilies = int(index.hFamilies.replace(',', ''))
        _hCouples = int(index.hCouples.replace(',', ''))
        _hSolo = int(index.hSolo.replace(',', ''))
        _hBusiness = int(index.hBusiness.replace(',', ''))
        _hFrineds = int(index.hFrineds.replace(',', ''))
        _hMarMay = int(index.hMarMay.replace(',', ''))
        _hJunAug = int(index.hJunAug.replace(',', ''))
        _hSepNov = int(index.hSepNov.replace(',', ''))
        _hDecFeb = int(index.hDecFeb.replace(',', ''))

        try:
            cursor.execute(
                "INSERT INTO HotelDetail(HotelId,excellent,verygood,average,poor,terrible,hFamilies,hCouples,hSolo,hBusiness,hFrineds,hMarMay,hJunAug,hSepNov,hDecFeb,TimeStamp) values ('" + _HotelId + "', '" + str(
                    _excellent) + "','" + str(_verygood) + "','" + str(_average) + "','" + str(_poor) + "','" + str(
                    _terrible) + "','" + str(_hFamilies) + "','" + str(_hCouples) + "','" + str(
                    _hSolo) + "','" + str(
                    _hBusiness) + "','" + str(_hFrineds) + "','" + str(_hMarMay) + "','" + str(
                    _hJunAug) + "','" + str(
                    _hSepNov) + "','" + str(_hDecFeb) + "','" + SystemTime + "')")
            cursor.commit()
            print(':::Insert to database successfully:::')
        except:
            print(':::Insert failed, please check!')

    HotelInfoList.clear()
    # =================================================================================================================================================================


# Step 2
# =================================================================================================================================================================
def Start_HotelReviewCrawler(list):
    skiptime = 0
    for index, i in enumerate(list):

        #skiptime = skiptime + 1
        #if skiptime < 9:
        #    continue
        _HotelId = i[2]
        _HotelUrl = i[4]

        print(' The hotel = ' + i[3])
        print(' The url = ' + _HotelUrl)

        DeltaReviewNum = -1

        TempList = HotelReviewCrawler.run_program(_HotelUrl, _HotelId, AreaId, SystemTime, DeltaReviewNum)

        ReviewList = TempList[0]
        ContentList = TempList[1]
        TravelList = TempList[2]
        # Insert to Database

        if len(ReviewList) != 0 and len(ContentList) != 0 and len(TravelList) != 0:
            print(':::Starting Insert to Database:::')
            cnt = 0
            for index in ReviewList:
                _ReviewId = index.ReviewId
                _UserId = index.UserId
                _AtPage = index.AtPage
                _OrderOfPage = str(index.OrderOfPage)
                _ReviewDate = index.ReviewDate
                print("\tRid={}\tUid={}\tAtPage={}\tOrder={}\tDate={}".format(_ReviewId, _UserId, _AtPage, _OrderOfPage,
                                                                              _ReviewDate))
                sql = "INSERT INTO ReviewOverview(HotelId, ReviewId,UserId,AtPage,OrderNumOfPage,ReviewDate,TimeStamp) values ('{}','{}','{}','{}','{}','{}','{}')"
                sql = sql.format(_HotelId, _ReviewId, _UserId, _AtPage, _OrderOfPage, _ReviewDate, SystemTime)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                except:
                    print(sql)
            for index in ContentList:
                _ReviewId = index.ReviewId
                _ReviewRating = index.ReviewRating.replace(',', '')
                _ReviewHelpfulvotes = index.ReviewHelpfulvotes.replace(',', '')
                print("\tRid={}\tRating={}\tVotes={}".format(_ReviewId, _ReviewRating, _ReviewHelpfulvotes))
                sql = "INSERT INTO ReviewScore(HotelId,ReviewId, ReviewRating,ReviewHelpfulvotes,TimeStamp) values ('{}','{}','{}','{}','{}')"
                sql = sql.format(_HotelId, _ReviewId, _ReviewRating, _ReviewHelpfulvotes, SystemTime)
                print(sql)

                try:
                    cursor.execute(sql)
                    cursor.commit()
                except:
                    print(sql)

                _ReviewTitle = index.ReviewTitle.replace(',', '@[CMA]').replace("'", "''")
                _ReviewContent = index.ReviewContent.replace(',', '@[CMA]').replace("'", "''")
                _Partial = index.Partial.replace(',', '@[CMA]').replace("'", "''").strip()

                
                emoji_pattern = re.compile("["
                                           u"\U0001F600-\U0001F64F"  # emoticons
                                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                           "]+", flags=re.UNICODE)
                _ReviewTitle = emoji_pattern.sub(r'', _ReviewTitle).encode().decode('ascii', 'ignore')
                _ReviewContent = emoji_pattern.sub(r'', _ReviewContent).encode().decode('ascii', 'ignore')
                _Partial = emoji_pattern.sub(r'', _Partial).encode().decode('ascii', 'ignore')

                try:
                    sql = "SELECT * FROM ReviewDetail WHERE ReviewId='{}'"
                    sql = sql.format(_ReviewId)
                    print(sql)
                    cursor.execute(sql)
                    CheckQuery = cursor.fetchall()
                except:
                    print(sql)

                if len(CheckQuery) == 0:
                    sql = "INSERT INTO ReviewDetail(ReviewId, ReviewTitle,ParitalContent,ReviewContent,TimeStamp) values ('{}','{}','{}','{}','{}')"
                    sql = sql.format(_ReviewId, _ReviewTitle, _Partial, _ReviewContent, SystemTime)
                    try:
                        cursor.execute(sql)
                        cursor.commit()
                    except:
                        print(sql)

            for index in TravelList:

                _HotelId = index['hotelid']
                _ReviewId = index['ReviewId']
                _TravelMonth = index['TravelMonth']
                _TravelType = index['TravelType']
                _PhotoCnt = index['PhotoCnt']

                cursor.execute(
                    "SELECT * FROM TravelType WHERE HotelId='" + _HotelId + "' AND ReviewId='" + _ReviewId + "'")
                CheckQuery = cursor.fetchall()

                if len(CheckQuery) == 0:
                    sql = "INSERT INTO TravelType(HotelId, ReviewId,TravelMonth,TravelType,PhotoCnt,TimeStamp) values ('{}','{}','{}','{}','{}','{}')"
                    sql = sql.format(_HotelId, _ReviewId, _TravelMonth, _TravelType, _PhotoCnt, SystemTime)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                except:
                    print(sql)


# step 3
# =================================================================================================================================================================

def Start_MemberProfileCrawler():
    # UserId='7EC2CD53AB6787D4C94E08F185E05483'
    # ReviewId='327918536'
    cursor.execute(
        "SELECT UserId,ReviewId FROM ReviewOverview WHERE TimeStamp='" + SystemTime + "'")
    QueryArray = cursor.fetchall()
    MemberProfileCrawler.run_program(QueryArray, SystemTime)


# *****************Main Program****************

SystemTime = Function.GetTimeStamp()
Yesterday = Function.GetYesterdayTimeStamp()

try:
    cursor = Function.DatabaseConnectionBuilder()
    print('[=Notification=] Database connection is built')
except:
    print('[=Notification=] Database connection occurs exception')
    SystemExit(0)

NY = 'http://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html'  # no.1
LV = 'http://www.tripadvisor.com/Hotels-g45963-Las_Vegas_Nevada-Hotels.html'  # no.2
OF = 'http://www.tripadvisor.com/Hotels-g34515-Orlando_Florida-Hotels.html'  # no.3
CI = 'http://www.tripadvisor.com/Hotels-g35805-Chicago_Illinois-Hotels.html'  # no.4
SF = 'https://www.tripadvisor.com/Hotels-g60713-San_Francisco_California-Hotels.html'  # no.5

CityArray = [('New York City, New York', NY), ('Chicago, Illinois', CI), ('San Francisco, California', SF),
             ('Orlando, Florida', OF), ('Las Vagas, Nevada', LV)]

CityArray = [('Orlando, Florida', OF)]

for CityElement in CityArray:
    # [Query Result]row=(1, 'New York', '60763')
    cursor.execute("SELECT * FROM AreaList WHERE AreaName='" + CityElement[0] + "'")

    row = cursor.fetchone()
    AreaId = str(row[0])
    CityName = CityElement[0]
    CityUrl = CityElement[1]

    print("[=Notification=] Now is [ {} ] running".format(CityName))

    cursor.execute("SELECT * FROM HotelList WHERE AreaId='" + AreaId + "'")
    HotelList = cursor.fetchall()

    print('[=Notification=] HotelInfoCrawler is Start')
    Start_HotelInfoCrawler(HotelList)
    print('[=Notification=] HotelInfoCrawler is finished')

    print('[=Notification=] HotelReviewCrawler is Start')
    Start_HotelReviewCrawler(HotelList)
    print('[=Notification=] HotelReviewCrawler is finished')

'''
print('[=Notification=] MemberProfileCrawler is Start')
Start_MemberProfileCrawler()
print('[=Notification=] MemberProfileCrawler is finished')
'''

cursor.close()
print('===Connection is closed===')
