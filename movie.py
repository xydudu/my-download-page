# encoding: UTF-8
#
import urllib2, re
from BeautifulSoup import BeautifulSoup

from google.appengine.ext import db
from google.appengine.api import memcache

from douban.service import DoubanService
from douban.client import OAuthClient

SERVER='api.douban.com'
API_KEY='0dfe7340ebe7ba4629fb59c2c3b72ed2'
SECRET='20055f18cc4bfe02'

class MovieData(db.Model):
    createTime = db.DateTimeProperty(auto_now = True )
    id = db.StringProperty()
    filename = db.StringProperty()
    link = db.StringProperty()
    intro = db.TextProperty()
    enintro = db.BlobProperty()
    dname = db.StringProperty()
    rate = db.StringProperty()
    imglink = db.StringProperty()


class Movie():
    sourceUrl = 'http://www.dy2018.com/'

    def getSource(self):
        req = urllib2.urlopen(self.sourceUrl)
        html = unicode(req.read(), 'gb2312','ignore').encode('utf-8','ignore')
        soup = BeautifulSoup(html)
        tds = soup('td', attrs={'width': '85%', 'height': '22', 'class': 'inddline'})
        o = [td.findAll('a')[1] for td in tds]
        #o = [(self.getID(a['href']), self.getName(a.string), a['href']) for a in o if re.search('BD', a.string) is not None]
        o = [(self.getID(a['href']), self.getName(a.string), a['href']) for a in o if re.search('1024', a.string) is not None]
        #for a in o:
        #    print a[1].encode('utf-8')
        return o

    def getName(self, str):
        return re.sub(u'.*?《(.*)》.*', r'\1', str)

    def getID(self, href):
        return re.findall('\d+\/\d+', href)[0]

    def saveToData(self, obj):
        if not self.hasData(obj[0]):
            m = self.getDoubanData(obj[1])
            ftplink = self.getDownlink(obj[2])
            if m != 0 and ftplink != 0:
                print type(ftplink.decode('utf-8'))
                print type(db.Text(obj[1]))
                db.put(MovieData(
                    id = obj[0],
                    filename = db.Text(obj[1]),
                    link = self.coverText(ftplink),
                    intro = self.coverText(m['intro']),
                    dname = self.coverText(m['name']),
                    rate = self.coverText(m['rate']),
                    imglink = m['img']
                ))
        else:
            print 'NO'

    def coverText(self, str):
        return db.Text(str.decode('utf-8'))
        
    def hasData(self, id):
         return len(db.GqlQuery("SELECT * FROM MovieData WHERE id = :1", id).fetch(1)) > 0

    def getListFormData(self):
        query = memcache.get('movielist')
        if query is None:
            sql = 'SELECT * FROM MovieData ORDER BY createTime DESC'
            query = db.GqlQuery(sql).fetch(20)
            memcache.add('movielist', query, 3600)
        return query

    def getDoubanData(self, keyword):
        keyword = keyword.encode('utf-8')
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
        
    def getDownlink(self, path):
        url = 'http://www.dy2018.com%s' % path 
        response = urllib2.urlopen(url)
        html = response.read()
        links = re.findall(r'>(ftp\:\/\/.*\.(?:rmvb|mkv))<', html)
        if len(links) > 0:
            return links[0].decode('gbk').encode('utf-8')
        else:
            return 0

if __name__ == '__main__':
    M = Movie()
    result = M.getSource()
    for i in result:
        M.saveToData(i)
