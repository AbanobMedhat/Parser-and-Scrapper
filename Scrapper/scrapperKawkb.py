from bs4 import BeautifulSoup
import requests
import csv


# global header
global header
header = {
'Host': 'www.autotrader.co.uk',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'close',
'Cookie': '__cfduid=d755139a43ab6bf4f420b5587b8056b401615041086; abtcid=94f2a934_db8f_4f75_acc7_4c897381f721; abTestGroups=FPAI-afvI-ahC-rxC-smT-ctI-fdT-gp3-hp0I-iosellC-nhT-orI-faT-rlI-ssA-search0I-spI-ucI-um0-ut0-uhT-usrI-viI; bucket=desktop; sessVar=940eed8e-81df-4530-8ae9-bfefcc345c33; userid=ID=1d5ba57e-ff2c-469c-be2a-fd25d5e6058e; user=STATUS=0&HASH=3f5734cd9c493e34f6454f76316d777e&PR=&ID=1d5ba57e-ff2c-469c-be2a-fd25d5e6058e; GeoLocation=Town=&Northing=&Latitude=51.556568272&Easting=&ACN=0&Postcode=E113LD&Longitude=0.0094344562; SearchData=postcode=E113LD; postcode=postcode=E113LD; searches=; cookiePolicy=seen.; LPCKEY-p-245=670f7fe6-9a60-44c0-aa9d-379ed86c29ca8-34561%7Cnull%7CindexedDB%7C120; CAOCID=3a6c4132-0e8f-4a9b-9631-b7f1c99120a60-73434; __cf_bm=b7581b13160e1b28f04383c0b07cf4281726ee0e-1615044079-1800-ARgBh4gYgph7csJV0UBx+RKng7wGokuHSEoG6IYHIYnew1/R9kOoYzTYc3NxhcjJQXP3SqGFDrg6kcopHOcJ0xk=; ctmQuickQuotes=%7B%7D'
}


# functions
# first search get max pages on results
def getPages():
    try:
        url = "https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=E113LD&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&include-delivery-option=on&page=1"
        rsp = requests.get(url, headers=header)
        rsp.raise_for_status()
        data = rsp.text
        parsed = BeautifulSoup(data, features="html.parser")
        countArr = parsed.find_all("li", class_="paginationMini__count")
        # the result of the find below return 7 as it's the index of "o" so to get the num add 3
        pageIndex = countArr[0].text.index("of") + 3
        maxPage = int(countArr[0].text[pageIndex:])
        return maxPage
    except requests.exceptions.Timeout:
        print("Error timeout")
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

# phone check function
def finalOutput(phoneNo):
    codeCheck = phoneNo[1:3]
    if (codeCheck == "07") or (codeCheck == "44"):
        return 1
    return 0


# save in csv file
def csvSave(csvWriter, sellerName, isTrade, PhoneNo):
    try:
        csvWriter.writerow([sellerName, isTrade, PhoneNo])
    except:
        print("Error in Writing in CSV")


# our result from the request (get name, phone, type)
def getRueslts(parsed, csvWriter):
    res1 = parsed.find_all("a", class_="js-click-handler listing-fpa-link tracking-standard-link")
    for i in range(0, len(res1)):
        temp = res1[i].attrs['href']
        carPage = temp[12:]
        prodUrl = "https://www.autotrader.co.uk/json/fpa/initial" + carPage
        try:
            newReq = requests.get(prodUrl, headers=header)
            newReq.raise_for_status()
            newReq = newReq.json()
            key = "name"
            # no name here is for the seller who hasn't name(blank name)
            if key in newReq["seller"].keys():
                sellerName = newReq["seller"]["name"]
            else:
                sellerName = "No Name"

            phoneNo = newReq["seller"]["primaryContactNumber"]
            isTrade = newReq["seller"]["isTradeSeller"]
            if finalOutput(phoneNo) == 1:
                csvSave(csvWriter, sellerName, isTrade, phoneNo)
        except requests.exceptions.Timeout:
                print("Error timeout")
        except requests.exceptions.HTTPError as err:
                raise SystemExit(err)


# main function for run the app and integrate functions
def main():
    try:
        csvFile = open('Results.csv', mode='a', newline="")
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Trade Name', 'Is Trade Seller', 'Phone Number'])
    except OSError:
        print("Can not open the file")
        exit()
    maxPage = getPages()
    # recommend putting fixed num instead of max pages as pages 50687 page
    for j in range(1, maxPage):
        print("page"+str(j)+": Opened")
        url = "https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=E113LD&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&include-delivery-option=on&page=" \
              + str(j)
        try:
            rsp = requests.get(url, headers=header)
            rsp.raise_for_status()
            data = rsp.text
            parsed = BeautifulSoup(data, features="html.parser")
            getRueslts(parsed, csvWriter)
        except requests.exceptions.Timeout:
            print("Error timeout")
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    csvFile.close()

# Main Function Call


main()

