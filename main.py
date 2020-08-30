import time
import random
from bs4 import BeautifulSoup
import requests
from datetime import datetime

today = datetime.today().strftime('%Y%m%d')



stock_url = {}
stock_data = []

path = today +'_usa_stock_price.csv'
f = open(path,'w')

header = ['company_name','ticker','market','price','industry','sector','prevclose','daysrange','revenue','open',
          'wk52range','eps','volume','marketcap','dividend_yield','averagevol_3m',
          'pe','beta','year1change','shares','nextearningsdate','crawling_YYYYMMDD']
row=''
for i in range(0, len(header)):
    row += header[i] + '\t'
row += '\n'
f.write(row)




with open("all_usa_stock_list.html", encoding="UTF8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    # ex_id_table = soup.findAll('table')[0]
    # print(ex_id_table.findAll('tr'))

    # 테이블에 있는 tr을 모두 가져온다.
    for tr in soup.findAll('table')[0].findAll('tr'):
        a_tag = tr.find_all('a', href=True)
        span_tag = tr.find_all('span')[1]
        for a in a_tag:
            #if a['title'].startswith('D'):
            stock_url[a['title']] = a['href']

print(stock_url)

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




    price = soup.findAll('div',class_='left current-data')[0].find('span',id='last_last').text
    market = soup.findAll('i',class_='btnTextDropDwn arial_12 bold')[0].text
    company_name_with_ticker = soup.findAll('div', class_='instrumentHead')[0].find('h1').text
    company_name = company_name_with_ticker[:company_name_with_ticker.index('(')-1]
    ticker = company_name_with_ticker[company_name_with_ticker.index('(')+1:company_name_with_ticker.index(')')]




    companyProfile = soup.findAll('div',class_='companyProfileHeader')
    if len(companyProfile) >0:
        industry = companyProfile[0].findAll('div')[0].findAll('a')[0].text
        sector = companyProfile[0].findAll('div')[1].findAll('a')[0].text
    else:
        industry ='N/A'
        sector ='N/A'



    # 그래프 하단 주가 정보
    div_tag = soup.findAll('div',class_='clear overviewDataTable overviewDataTableWithTooltip')[0]

    span_tag = div_tag.findAll('span',class_='float_lang_base_2 bold')



    # company_name
    stock_data.append(company_name)
    # Input ticker
    stock_data.append(ticker)
    # Input Market
    stock_data.append(market)
    # Input Price
    stock_data.append(price)
    # Input Industry
    stock_data.append(industry)
    # Input Sector
    stock_data.append(sector)

    # Input all data got above to dict
    for s in span_tag:
         info = s.text
         stock_data.append(info)

    # Input Today
    stock_data.append(today)
    print(stock_data)

    # write csv
    row = ''
    for i in range(0, len(stock_data)):
        row += stock_data[i].replace(',','')+'\t'

    row += '\n'
    f.write(row)
    print(row)
    stock_data.clear()

f.close()

