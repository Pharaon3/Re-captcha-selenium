import time
from bs4 import BeautifulSoup
import requests
from lptag import Lptag

def get_ids(html):
    c_id = html[html.find('"customerId": ')+15:html.find('"customerId": ')+22]
    soup = BeautifulSoup(html)
    title = soup.find('title').get_text().strip()
    asf = soup.find('input', {'name':'as_sfid'}).get('value')
    af = soup.find('input', {'name':'as_fid'}).get('value')
    a = soup.findAll('img')
    links = []
    print('as')
    for i in a:
        links.append(i.get('src'))
    return asf, af, title, c_id,links

ses = requests.session()
ses.proxies.update({'http':'http://user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000', 'https':'http://user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000'})

headers = {
'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': "en-US,en;q=0.9",
'Connection': 'keep-alive',
'Host': 'www.answerfinancial.com',
'referer': 'https://www.answerfinancial.com/',
'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "macOS",
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
r = ses.get("https://www.answerfinancial.com/", headers=headers)

asf, af, title, customer_id, links= get_ids(r.text)
lptag = Lptag()
lptag.start_session(customer_id, title, "https://www.answerfinancial.com/")
cookie_obj = requests.cookies.create_cookie(domain=".answerfinancial.com", name="LPSID-48853463", value=lptag.session_id)
cookie_obj1 = requests.cookies.create_cookie(domain=".answerfinancial.com", name="LPVID", value=lptag.visitor_id)
ses.cookies.set_cookie(cookie_obj)
ses.cookies.set_cookie(cookie_obj1)
print(ses.cookies.get_dict().keys())

# headers['Accept'] ="image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
# for i  in links[:5]:
#     if not str(i).startswith('/C'):
#         continue
#     r = ses.get('https://www.answerfinancial.com'+i, headers=headers, cookies=ses.cookies)
#     print(r.status_code)

lptag.refresh_token()
data ={'Temp.IntroZipCode': '72687',
'as_sfid': asf,
'as_fid': af,
'X-Requested-With': 'XMLHttpRequest'}

ses.post("https://www.answerfinancial.com/auto/landingzipsequence", json=data)
time.sleep(1)
r = ses.get("https://www.answerfinancial.com/auto/basicinfo", headers=headers)
asf, af, title, customer_id , links= get_ids(r.text)
# lptag.next_pagepage(customer_id, title, "https://www.answerfinancial.com/auto/basicinfo", "https://www.answerfinancial.com/")
# lptag.page_loaded()

r = ses.get("https://www.answerfinancial.com/Avs/CityAutoComplete?zipcode=72687", headers=headers)
print(r.status_code)

data = {'Persons__0.FirstName': 'FRED',
'Persons__0.LastName': 'HILDEBRAND',
'Vehicles__0.V_Address': 'THOUSAND OAKS RD',
'Vehicles__0.V_Unit': '',
'Vehicles__0.V_ZipCode': '72687',
'Vehicles__0.V_State': 'AR',
'Vehicles__0.V_City': 'YELLVILLE',
'Persons__0.DOB': '08/23/1947',
'as_sfid': asf,
'as_fid': af,
'X-Requested-With': 'XMLHttpRequest'}
r = ses.post("https://www.answerfinancial.com/auto/basicinfo/0", data=data, headers=headers)
print(r.status_code)
print(r.content)

r = ses.get("https://www.answerfinancial.com/auto/vehiclesmatch/0", headers=headers)
print(r.status_code)
print(r.text)
# asf, af, title, customer_id = get_ids(r.text)
# lptag.next_page(customer_id, title, "https://www.answerfinancial.com/auto/vehicleinfo/0", "https://www.answerfinancial.com/auto/basicinfo")
