import time
import random

from bs4 import BeautifulSoup
import urllib.request
import requests

stock_url = {}
stock_info = {}
with open("all_usa_stock_list.html", encoding="UTF8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    # ex_id_table = soup.findAll('table')[0]
    # print(ex_id_table.findAll('tr'))

    # 테이블에 있는 tr을 모두 가져온다.
    for tr in soup.findAll('table')[0].findAll('tr'):
        a_tag = tr.find_all('a', href=True)
        span_tag = tr.find_all('span')[1]
        for a in a_tag:
            stock_url[a['title']] = a['href']
            stock_info[a['title'].lower()] = [span_tag['data-name']]

cnt = 0
for k, v in stock_url.items():


    # Setting User-Agent for crawling
    headers ={'accept':"text/html",
              'User-Agent' :'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'
              }

    # get HTML
    r = requests.get(v,headers=headers)

    print(r.status_code)

    # HTML Parsing
    soup = BeautifulSoup(r.text, 'html.parser')



    company_name_with_ticker = soup.findAll('div',class_='instrumentHead')[0].find('h1').text
    print(company_name_with_ticker)


    company_name = company_name_with_ticker[:company_name_with_ticker.index('(')-1]
    ticker = company_name_with_ticker[company_name_with_ticker.index('(')+1:company_name_with_ticker.index(')')]

    print(company_name)
    print(ticker)

    # ticker input
    stock_info[company_name.lower()].append(ticker)

    # get All div tag
    div_tag = soup.findAll('div',class_='clear overviewDataTable overviewDataTableWithTooltip')[0]

    span_tag = div_tag.findAll('span')

    # get stock information
    for i,s in enumerate(span_tag):
        info = s.text

        stock_info[company_name.lower()].append(info)

    sec = int(random.uniform(1,5))
    time.sleep(sec)
    print(stock_info[company_name.lower()])

    cnt +=1
    if cnt == 2:
        break
    # company_nm , company_ticker, info_cd , info_value
f = open('data.csv','w')
for k,v in stock_info.items():
    company_nm_ticker = v[0] +'|' +v[1]

    for i in range(2,len(v)):
        row =''
        if i%2 == 0 :
            row += company_nm_ticker +'|' +v[i] +'|' + v[i+1].replace(',','') +'\n'
            f.write(row)


f.close()

