# encoding: UTF-8

import urllib, re, zipfile, os, time

from google.appengine.ext import webapp
from google.appengine.ext import db
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
        service = DoubanService(api_key=API_KEY,secret=SECRET)
        feed = service.SearchMovie(keyword)
        movie = service.GetMovie(feed.entry[0].id.text)
        
        return { 
            'name': movie.title.text,
            'intro': movie.summary.text,        
            'rate': movie.rating.average,
            'img': movie.link[2].href
        }
    
    def dygod(self):
        url = 'http://www.dygod.org/html/gndy/dyzz/index.html'
        req = urllib.urlopen(url)
        #names = re.findall(r'<a\ href\=\".*"\ class\=\"ulink\".*《(.*)》.*BD.*>', req.read())
        regex = r'<a\ href\=\"(.*)"\ class\=\"ulink\">(.*).*?BD.*>'
        names = re.findall(regex, req.read())

        return names

    def getDownloadLinks(self, path):
        url = 'http://www.dygod.org%s' % path 
        response = urllib.urlopen(url)
        html = response.read()
        links = re.findall(r'>(ftp\:\/\/.*\.(?:rmvb|mkv))<', html)
        return links[0].decode('gbk').encode('utf-8')

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
            html += '<h3>%s</h3>' % o['name']
            html += '<div class="box">'
            html += '<img src="%s" />' % o['img']
            html += '<p style="color:red;">rate from douban : %s </p>' % o['rate']
            html += '<p>intro : %s </p>' % o['intro']
            html += '<p style="color:blue; font-size:11px">%s</p>' % self.getDownloadLinks(key[0])
            html += '</div>'

        html += '''
            <hr />
            <div class="foot">Not for public, please do not tell anyone!</div>
            </body></html>
        '''
        return html
        
    def showHTML(self):
        today = time.strftime('%Y%m%d')
        filename = r'backup'+ os.sep + today + '.data'
            
        html = FileData.all().filter("id =", today).fetch(1)
        print len(html)
        if len(html) > 0:
            print html[0].content
        else:
            content = self.getHTML()
            item = FileData(html = content, id = today)
            db.put(item)
            print content

if __name__ == '__main__':
    m = movies()
    m.showHTML()
