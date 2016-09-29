import HotelListCrawler
import Function


def Start_HotelListCrawler(url, AreaId):
    HotelList = HotelListCrawler.run_program(url)
    for i in range(0, 10, 1):
        _HotelName = HotelList[i].Name.replace(',', '@[CMA]').replace("'", "''")
        _HotelHref = HotelList[i].Href.replace(',', '@[CMA]').replace("'", "''")
        cursor.execute(
            "INSERT INTO HotelList(AreaId, HotelId,HotelName,HotelHref) values ('" + AreaId + "', '" + HotelList[
                i].Id + "','" + _HotelName + "','" + _HotelHref + "')")
        cursor.commit()

    HotelList.clear()


def IntialAllHotelList(CityArray):
    print('[Step]Intial All HotelList')

    for CityElement in CityArray:
        # [Query Result]row=(1, 'New York', '60763')

        cursor.execute("SELECT * FROM AreaList WHERE AreaName='" + CityElement[0] + "'")

        row = cursor.fetchone()
        AreaId = str(row[0])
        CityUrl = CityElement[1]

        Start_HotelListCrawler(CityUrl, AreaId)

    print('[Step]Finish Intialization')


# *****************Main Program****************

SystemTime = Function.GetTimeStamp()

try:
    cursor = Function.DatabaseConnectionBuilder()
    print('[=Notification=] Database connection is built')
except:
    print('[=Notification=] Database connection occurs exception')
    SystemExit(0)

# Step 1 (Get Hotel List From Current Area)

NY = 'http://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html'  # no.1
LV = 'http://www.tripadvisor.com/Hotels-g45963-Las_Vegas_Nevada-Hotels.html'  # no.2
OF = 'http://www.tripadvisor.com/Hotels-g34515-Orlando_Florida-Hotels.html'  # no.3
CI = 'http://www.tripadvisor.com/Hotels-g35805-Chicago_Illinois-Hotels.html'  # no.4
SF = 'https://www.tripadvisor.com/Hotels-g60713-San_Francisco_California-Hotels.html'  # no.5

CityArray = [('New York City, New York', NY), ('Las Vagas, Nevada', LV), ('Orlando, Florida', OF),
             ('Chicago, Illinois', CI), ('San Francisco, California', SF)]

IntialAllHotelList(CityArray)

cursor.close()
print('===Connection is closed===')
