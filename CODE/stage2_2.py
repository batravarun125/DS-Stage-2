import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup as soup
import re
import sys
import time


agent = requests.utils.default_headers()
agent.update({
    "User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
})

# Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36
agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
#agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
#arr = ["https://www.amazon.com/s?k=fiction&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=mystery&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=mystery&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=sex&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=dating&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=religion&i=stripbooks&ref=nb_sb_noss"]
arr = ["https://www.amazon.com/s?k=love&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=sex&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=religion&i=stripbooks&ref=nb_sb_noss"]

mainPage = requests.get(arr[0], headers=agent)
arr_count = 1
csv = open("test_var.csv", "w", encoding='utf=8')
f = open("mainPage_2.txt", "w", encoding='utf=8')
f1 = open("bookPage_2.txt", "w", encoding='utf=8')
csv.write("title, author, rating, format, price, year\n")

f.write(str(mainPage.content))

count = 0
while mainPage.status_code == 200:
    # print(arr[0])
    parsed = soup(mainPage.content, 'html.parser')
    #print(parsed)
    mainPage.close()
    print(parsed.findAll("div",{"class":"sg-row"}))
    books = parsed.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
    #books = parsed.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
# sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
# sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    # sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    print(len(books))
    # f1.write(str(books[0]))

    for i in range(0,len(books)):
        title = books[i].find("h5", {"class":"a-color-base s-line-clamp-2"}).find("span", "a-size-medium a-color-base a-text-normal")
        print(title.text)
        year = books[i].find("span", {"class":"a-size-base a-color-secondary a-text-normal"})
        if year == None:
            year = ''
        else:
            year = year.text.split(' ')
            if (len(year) == 3):
                year = year[2]
            else:
                year = ''
        print("Year: " + year)
        authorName = books[i].find("div", {"class":"a-row a-size-base a-color-secondary"})
        #correct this as sometimes if no author name means not a book
        
        if (authorName == None):
            authorName = ''
        else:
            authorName = authorName.find("a","a-size-base a-link-normal")
            if (authorName == None):
                authorName = ''
            else :
                authorName = authorName.text.strip()
                print(authorName)
        bookFormat = books[i].find("div",{"class":"a-row a-size-base a-color-base"}).find("a",{"class":"a-size-base a-link-normal a-text-bold"})
        
        print("bc")    
        if bookFormat == None:
            bookFormat = ''
        else:
            bookFormat = bookFormat.text.strip()
        print("format: " + bookFormat)

        rating = books[i].find("span", {"class":"a-icon-alt"})
        if(rating==None):
            rating = ''
        else:
            rating = rating.text
        
        print("Rating: " + rating)
        p1 = books[i].find("div", {"class":"a-section a-spacing-none a-spacing-top-small"})
        price = p1.find("span", {"class":"a-price-whole"})
        priceDecimal = books[i].find("span", {"class":"a-price-fraction"})
        
        if price == None:
            price = ''
        else:
            price = price.text
            price = re.sub('[,]', '', price)
        if priceDecimal==None:
            priceDecimal = ''
        else:
            priceDecimal = priceDecimal.text
        price = price + priceDecimal
        print("Price: " + price)

        ans = str(title.text).replace(",", "~") + "," + str(authorName).replace(",", "~") + "," + str(rating).replace(",", "~") + "," + str(bookFormat).replace(",", "~") + "," + str(price).replace(",", "~") + "," + str(year).replace(",", "~") +"\n"
        csv.write(ans)
        # with csv:
        #     spamwriter = csv.writer(csv, delimiter='~')
        #     spamwriter.writerow(ans)
        count = count + 1
        print("Book " + repr(count))


    if (count > 500 ):
        break
    p = parsed.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-last"})
    if ((count % 50) == 0):
            time.sleep(4)
    print(p)
    
    # if parsed.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-disabled a-last"})!=None:
    #     mainPage = requests.get(arr[arr_count], headers=agent)
    #     arr_count=arr_count+1
    #     parsed = soup(mainPage.content, 'html.parser')
    # # print(parsed)
    #     mainPage.close()
    #     books = parsed.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
    #     print(len(books))
    
    # else:
    p = parsed.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-last"}).find("a")["href"]
    print (p)
    nextLink = "https://www.amazon.com" + p
    print(nextLink)
    if ((count % 50) == 0):
        time.sleep(4)
    mainPage = requests.get(nextLink, headers=agent)

csv.close()
