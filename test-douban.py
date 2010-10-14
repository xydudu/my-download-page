# encoding: UTF-8

import urllib2, re, time

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import memcache

from douban.service import DoubanService
from douban.client import OAuthClient

SERVER='api.douban.com'
API_KEY='0dfe7340ebe7ba4629fb59c2c3b72ed2'
SECRET='20055f18cc4bfe02'

class FileData(db.Model):
    createTime = db.DateTimeProperty(auto_now = True )
    id = db.StringProperty(required = True )
    html = db.BlobProperty(required = True)

class movies():

    def douban(self, keyword):
        keyword = keyword.decode('gbk').encode('utf-8')
        keyword = re.sub(r'.*?《(.*)》', r'\1', keyword)
        service = DoubanService(api_key=API_KEY,secret=SECRET)
        feed = service.SearchMovie(keyword)
        if len(feed.entry) > 0:
            movie = service.GetMovie(feed.entry[0].id.text)
            return { 
                'name': movie.title.text,
                'intro': movie.summary.text,        
                'rate': movie.rating.average,
                'img': movie.link[2].href
            }
        else:
            return 0
        
    
    def dygod(self):
        url = 'http://www.dy2018.com/'
        req = urllib2.urlopen(url)
        #names = re.findall(r'<a\ href\=\".*"\ class\=\"ulink\".*《(.*)》.*BD.*>', req.read())
        #regex = r'<a\ href\=\"(.*)"\ class\=\"ulink\">(.*).*?BD.*>'
        regex = r'\]<a\ href\=\'(.*?)\'.*>(\S+?)BD.*?<'
        names = re.findall(regex, req.read())
        return names

    def getDownloadLinks(self, path):
        url = 'http://www.dy2018.com%s' % path 
        response = urllib2.urlopen(url)
        #print url
        html = response.read()
        #print html
        links = re.findall(r'>(ftp\:\/\/.*\.(?:rmvb|mkv))<', html)
        if len(links) > 0:
            return links[0].decode('gbk').encode('utf-8')
        else:
            return 0

    def getHTML(self):
        keys = self.dygod()
        html = '''
            <!doctype html>
            <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>movies by dudu</title>
            <style>
                p { margin:0; padding:0}
                .foot {font-size:12px; color:gray}
                .box { overflow: hidden }
                img { float:left; left: 0; top: 0; }
                p { padding: 0 0 5px 100px }
            </style>
            <body>
            <h1>电影下载</h1>
        '''    
        for key in keys:
            o = self.douban(key[1])
            downlink = self.getDownloadLinks(key[0])
            if o != 0 and downlink != 0: 
                html += '<h3>%s</h3>' % o['name']
                html += '<div class="box">'
                html += '<img src="%s" />' % o['img']
                html += '<p style="color:red;">rate from douban : %s </p>' % o['rate']
                html += '<p>intro : %s </p>' % o['intro']
                html += '<p style="color:blue; font-size:11px">%s</p>' % downlink
                html += '</div>'

        html += '''
            <hr />
            <div class="foot">Not for public, please do not tell anyone!</div>
            </body></html>
        '''
        return html
        
    def showHTML(self):
        today = time.strftime('%Y%m%d')
        
        #memcache.delete(today)
        html = memcache.get(today)
        if html is not None:
            print html
        else:
            html = self.getHtmlFromData(today)
            if not memcache.add(today, html, 36000):
                logging.error("Memcache set failed.")
            print html
    
    def getHtmlFromData(self, today):
        
        html = FileData.all().filter("id = ", today).fetch(1)
        if len(html) > 0:
            return html[0].html
        else:
            content = self.getHTML()
            item = FileData(html = content, id = today)
            db.put(item)
            return content
        return self.getHTML()
        

if __name__ == '__main__':
    m = movies()
    m.showHTML()
