from bs4 import BeautifulSoup
import urllib3
import random

class Client():
    
    def __init__(self, proxies=None):
        if isinstance(proxies, type(None)):
            self.proxies = None
        elif isinstance(proxies, str):
            self.proxies = [proxies]
        elif isinstance(proxies, list):
            self.proxies = proxies
        
        self.http = urllib3.PoolManager()

    def search(self, q, **kwargs):
        if self.proxies:
            proxy = random.choice(self.proxies)
            http = urllib3.ProxyManager(proxy)
        else:
            http = self.http
        r = http.request("get","https://www.bing.com/search", fields=dict(q=q, **kwargs))
        return sr(r.data)
    
    def image(self, q, **kwargs):
        if self.proxies:
            proxy = random.choice(self.proxies)
            http = urllib3.ProxyManager(proxy)
        else:
            http = self.http
        r = http.request("get","https://www.bing.com/images/search", fields=dict(q=q, **kwargs))
        return sr_im(r.data)
  
def sr(data):
    a = []
    soup = BeautifulSoup(data, "html.parser")
    results = soup.find("ol", {"id":"b_results"})
    lists = results.findAll("li", {"class":"b_algo"})
    for item in lists:
        item_text = item.find("a").text
        item_href = item.find("a").attrs["href"]
        if item_text and item_href:
            a.append({"title":item_text,"url":item_href})
    return a

def sr_im(data):
    a = []
    soup = BeautifulSoup(data, "html.parser")
    links = soup.findAll("a", {"class":"thumb"})
    for item in links:
        a.append({"title":item["href"].split("/")[-1],"url":item.attrs["href"]})
    return a