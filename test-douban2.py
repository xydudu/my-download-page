# encoding: UTF-8

import urllib, re
from douban.service import DoubanService
from douban.client import OAuthClient

SERVER='api.douban.com'
API_KEY='0dfe7340ebe7ba4629fb59c2c3b72ed2'
SECRET='20055f18cc4bfe02'

class movies():

    def douban(self, keyword):
        print keyword
        service = DoubanService(api_key=API_KEY,secret=SECRET)
        feed = service.SearchMovie(keyword)
        movie = service.GetMovie(feed.entry[0].id.text)
        
        return { 
            'name': movie.title.text,
            'intro': movie.summary.text,        
            'rate': movie.rating.average
        }
    
    def dygod(self):
        url = 'http://www.dygod.org/html/gndy/dyzz/index.html'
        req = urllib.urlopen(url)
        names = re.findall(r'<a\ href\=\".*"\ class\=\"ulink\".*¡¶(.*)¡·.*BD.*>', req.read())
        #for i in names:
        #   print i
        return names

if __name__ == '__main__':
    m = movies()
    keys = m.dygod()
    for key in keys:
        print m.douban(key)
        
