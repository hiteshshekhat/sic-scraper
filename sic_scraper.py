from unicodedata import category
import requests
import requests_cache
from time import time, sleep
import random
from bs4 import BeautifulSoup

requests_cache.install_cache(expire_after=18000, allowable_methods=('GET', 'POST'))


with open("proxies_ip.txt", "r") as f:
    proxies=f.read().splitlines()


def send_request(url, proxies):
    while True:
        proxy = proxies[random.randint(0, len(proxies)-1)]
        try:
            # proxies = {"http": 'http://' + proxies(proxy), "https": 'https://' + proxies(proxy)}
            response = requests.get(url, timeout=5, proxies={"http": 'http://' + proxy, "https": 'https://' + proxy})
            print(response.status_code)
            print("Proxy currently being used")
            break
        except:
            print("Error, looking for another proxy")
    return response

def get_last_page_number(url):
    r = send_request(url, proxies)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    page_div_text = html_soup.find('div', {'class':'pageNav'}).get_text()
    print(page_div_text)
    total_page = int(page_div_text.split(' ')[3])
    return total_page


category_url = 'http://www.siclists.com/sic-code.html'



r = requests.get(category_url)
html_soup = BeautifulSoup(r.text, 'html.parser')
category_li = html_soup.select('.statelistss ul li a')
category_urls = [a['href'] for a in category_li]
category_dict = {a['href'] : a.get_text(strip=True) for a in category_li}
print(category_urls)
print(category_dict)


for url in category_urls[0:1]:
    total_pages = get_last_page_number(url)
    for i in range(1):
        if i > 0:
            cat_url = url[:-5] + '-' + str(random.randint(1, total_pages)) + url[-5:]
        else:
            cat_url = url
        print(cat_url)
        r = send_request(cat_url, proxies)
        html_soup = BeautifulSoup(r.text, 'html.parser')
        a_tags = html_soup.select('.boxcon tr:nth-of-type(1) a')
        # print(a_tags)
        for a in a_tags[0:1]:
            company_url = a['href']
            company_dict = {'seen_url':company_url, 'seen_epoch': time(), 'company_name':a.get_text(strip=True)}
            print(company_dict)
            r = send_request(company_url, proxies)
            html_soup = BeautifulSoup(r.text, 'html.parser')
            info = html_soup.select('.infolist li')

            print(info)





