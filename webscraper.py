import io
import requests
import pandas as pd
from bs4 import BeautifulSoup

def PennyStocks():
    r = requests.get('http://openinsider.com/latest-penny-stock-buys')
    soup = BeautifulSoup(r.content, 'html.parser')
    stringData = str(soup.get_text(separator=" "))[2502:]


    stringData = stringData.replace("   ", "\n")
    stringData = stringData.replace(" - ", "\n")

    newString = io.StringIO(stringData)
    lst = newString.readlines()[0:300]

    filingDate = []
    tradeDate = []
    ticker = []
    nums = []
    price = []
    qty = []
    totalOwned = []
    deltaOwned = []
    deltaValue = []
    titleList = ["CEO","COO","CFO","COB","Pres","10%","Dir","GC","Secretary","EVP","Treasurer"]
    title = []
    infoList = []

    for x in lst:
        y = lst.index(x)
        infoMapping = {" M ":"",
                    " AM ":"",
                    " AD ":"",
                    " A ":"",
                    " D ":"",
                    " DM ":","}
        #if x[0] == " ":
        #    lst[y] = lst[y].translate(infoMapping)
        
        
        if x[0] == " ":
            if " M " in x:
                lst[y] = lst[y].replace(' M ', "")
            elif " AM " in x:
                lst[y] = lst[y].replace(" AM ", "")
            elif " AD " in x:
                lst[y] = lst[y].replace(" AD ", "")
            elif " A " in x:
                lst[y] = lst[y].replace(" A ", "")
            elif " D " in x:
                lst[y] = lst[y].replace(" D ", "")
            elif " DM " in x:
                lst[y] = lst[y].replace(" DM ", "")
            else:
                lst[y] = lst[y][1:]
        
        if "\n" in x:
            lst[y] = lst[y].replace("\n", "")

        if lst[y][0:4] == '2025':
            filingDate.append(lst[y][0:19])
            tradeDate.append(lst[y][20:])

        if lst[y][0:4] != '2025' and lst[y][0:8] != "Purchase":
            ticker.append(lst[y].partition(" ")[0])
            infoList.append(lst[y])
            
        
        if lst[y][0:8] == "Purchase":
            lst[y] = lst[y].replace(",", "")
            lst[y] = lst[y].replace("+", "")
            lst[y] = lst[y].replace("%", "")
            lst[y] = lst[y].replace("$", "")
            lst[y] = lst[y].replace(" ",",")
            nums = lst[y].split(",")
            price.append(nums[1])
            qty.append(nums[2])
            totalOwned.append(nums[3])
            deltaOwned.append(nums[4])
            deltaValue.append(nums[5])

    for t in infoList:
        subTitle = []
        for s in titleList:
            if s in t:
                subTitle.append(s)
        title.append(subTitle)
            
    df = pd.DataFrame({"Filing Date":filingDate,
                    "Trade Date":tradeDate,
                    "Ticker": ticker,
                    "Title":title,
                    "Price":price,
                    "Quantity":qty,
                    "Total Owned":totalOwned,
                    "Delta Owned":deltaOwned,
                    "Delta Value":deltaValue})


    pd.set_option('display.max_columns', None)
    return df

#def storeDF():


def main():
    newDF = PennyStocks()
    print(newDF)

if __name__ == "__main__":
    main()